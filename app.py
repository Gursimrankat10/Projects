import json
import os
import re
import secrets
import sqlite3
from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from careers import (
    CAREERS,
    DIMENSION_LABELS,
    QUESTIONS,
    daily_tasks_for_career,
    tasks_for_career,
    video_recommendations,
)
from mentor_engine import classify_intent, mentor_reply


BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("DATABASE_PATH", str(BASE_DIR / "career_compass.db")))
SECRET_KEY_FILE = BASE_DIR / ".career_compass_secret"
LEGACY_TABLES = ("progress", "assessments", "task_completions", "mentor_messages")


def load_secret_key(path=SECRET_KEY_FILE):
    configured_secret = os.environ.get("SECRET_KEY")
    if configured_secret:
        return configured_secret
    try:
        secret = path.read_text(encoding="ascii").strip()
    except FileNotFoundError:
        secret = secrets.token_hex(32)
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            secret = path.read_text(encoding="ascii").strip()
        else:
            with os.fdopen(descriptor, "w", encoding="ascii") as secret_file:
                secret_file.write(secret)
                secret_file.write("\n")
    if len(secret) < 64:
        raise RuntimeError(f"The Flask session secret in {path} is invalid.")
    return secret


app = Flask(__name__)
app.config.update(
    SECRET_KEY=load_secret_key(),
    MAX_CONTENT_LENGTH=16 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(days=365),
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


def table_exists(database, table_name):
    return database.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone() is not None


def init_db():
    database = get_db()
    for table in LEGACY_TABLES:
        if not table_exists(database, table):
            continue
        columns = {
            row["name"] for row in database.execute(f"PRAGMA table_info({table})")
        }
        legacy_name = f"legacy_{table}"
        if table == "progress" or "user_id" not in columns:
            if table_exists(database, legacy_name):
                raise RuntimeError(f"Both {table} and {legacy_name} exist; resolve the database migration manually.")
            database.execute(f"ALTER TABLE {table} RENAME TO {legacy_name}")

    database.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            display_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            theme TEXT NOT NULL DEFAULT 'dark' CHECK (theme IN ('dark', 'light')),
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            xp INTEGER NOT NULL DEFAULT 0,
            streak INTEGER NOT NULL DEFAULT 0,
            last_active TEXT,
            selected_career TEXT
        );
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            scores TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS assessments_user_created
            ON assessments(user_id, created_at);
        CREATE TABLE IF NOT EXISTS task_completions (
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            task_id TEXT NOT NULL,
            completed_on TEXT NOT NULL,
            PRIMARY KEY (user_id, task_id, completed_on)
        );
        CREATE TABLE IF NOT EXISTS daily_task_plans (
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            plan_date TEXT NOT NULL,
            task_ids TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (user_id, plan_date)
        );
        CREATE TABLE IF NOT EXISTS mentor_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role TEXT NOT NULL CHECK (role IN ('user', 'mentor')),
            message TEXT NOT NULL,
            sources TEXT NOT NULL DEFAULT '[]',
            intent TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS mentor_messages_user_id ON mentor_messages(user_id, id);
        """
    )
    database.execute(
        "INSERT OR IGNORE INTO user_progress (user_id) SELECT id FROM users"
    )
    database.commit()


def migrate_legacy_data(database, user_id):
    if table_exists(database, "legacy_progress"):
        columns = {
            row["name"] for row in database.execute("PRAGMA table_info(legacy_progress)")
        }
        rows = (
            database.execute("SELECT * FROM legacy_progress").fetchall()
            if "user_id" in columns
            else [database.execute("SELECT * FROM legacy_progress LIMIT 1").fetchone()]
        )
        for row in rows:
            if row:
                target_user_id = row["user_id"] if "user_id" in columns else user_id
                database.execute(
                    """UPDATE user_progress SET xp = ?, streak = ?, last_active = ?,
                       selected_career = ? WHERE user_id = ?""",
                    (
                        row["xp"],
                        row["streak"],
                        row["last_active"],
                        row["selected_career"],
                        target_user_id,
                    ),
                )
    if table_exists(database, "legacy_assessments"):
        for row in database.execute("SELECT scores, created_at FROM legacy_assessments"):
            database.execute(
                "INSERT INTO assessments (user_id, scores, created_at) VALUES (?, ?, ?)",
                (user_id, row["scores"], row["created_at"]),
            )
    if table_exists(database, "legacy_task_completions"):
        for row in database.execute("SELECT task_id, completed_on FROM legacy_task_completions"):
            database.execute(
                "INSERT OR IGNORE INTO task_completions (user_id, task_id, completed_on) VALUES (?, ?, ?)",
                (user_id, row["task_id"], row["completed_on"]),
            )
    if table_exists(database, "legacy_mentor_messages"):
        for row in database.execute(
            "SELECT role, message, created_at FROM legacy_mentor_messages ORDER BY id"
        ):
            database.execute(
                """INSERT INTO mentor_messages
                   (user_id, role, message, sources, created_at)
                   VALUES (?, ?, ?, '[]', ?)""",
                (user_id, row["role"], row["message"], row["created_at"]),
            )
    for table in LEGACY_TABLES:
        legacy_name = f"legacy_{table}"
        if table_exists(database, legacy_name):
            database.execute(f"DROP TABLE {legacy_name}")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Sign in to save and view your career progress.", "info")
            return redirect(url_for("login"))
        user = get_db().execute(
            "SELECT id FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        if user is None:
            session.clear()
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def current_progress():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_db().execute(
        "SELECT * FROM user_progress WHERE user_id = ?", (user_id,)
    ).fetchone()


def selected_career_id(progress):
    if progress is None:
        return None
    try:
        return progress["selected_career"]
    except (TypeError, KeyError):
        return None


def daily_task_plan(user_id, career, plan_date=None):
    database = get_db()
    plan_date = plan_date or date.today()
    day_key = plan_date.isoformat()
    saved_plan = database.execute(
        "SELECT task_ids FROM daily_task_plans WHERE user_id = ? AND plan_date = ?",
        (user_id, day_key),
    ).fetchone()
    if saved_plan:
        task_ids = json.loads(saved_plan["task_ids"])
        available = {task["id"]: task for task in tasks_for_career(career)}
        if all(task_id in available for task_id in task_ids):
            return [available[task_id] for task_id in task_ids]

    assessment = latest_assessment(user_id)
    recent_task_ids = [
        row["task_id"]
        for row in database.execute(
            """SELECT task_id FROM task_completions
               WHERE user_id = ? AND completed_on >= ? AND completed_on < ?
               ORDER BY completed_on DESC""",
            (user_id, (plan_date - timedelta(days=7)).isoformat(), day_key),
        ).fetchall()
    ]
    selected_tasks = daily_tasks_for_career(
        career,
        user_id,
        plan_date,
        assessment["scores"] if assessment else None,
        recent_task_ids,
    )
    database.execute(
        """INSERT OR REPLACE INTO daily_task_plans
           (user_id, plan_date, task_ids, created_at) VALUES (?, ?, ?, ?)""",
        (
            user_id,
            day_key,
            json.dumps([task["id"] for task in selected_tasks]),
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    database.commit()
    return selected_tasks


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@app.context_processor
def inject_template_helpers():
    return {
        "csrf_token": csrf_token,
        "today": date.today().isoformat(),
        "current_progress": current_progress,
        "current_user": current_user,
    }


def verify_csrf():
    if not secrets.compare_digest(
        str(request.form.get("csrf_token", "")), str(session.get("csrf_token", ""))
    ):
        abort(400, description="Your form session expired. Refresh the page and try again.")


def career_by_id(career_id):
    if isinstance(career_id, dict):
        career_id = career_id.get("id")
    if not career_id:
        return None
    return next((career for career in CAREERS if career["id"] == career_id), None)


def latest_assessment(user_id):
    row = get_db().execute(
        "SELECT scores, created_at FROM assessments WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,),
    ).fetchone()
    if row is None:
        return None
    return {"scores": json.loads(row["scores"]), "created_at": row["created_at"]}


def ranked_careers(scores):
    ranked = []
    for career in CAREERS:
        dimensions = career["dimensions"]
        total_weight = sum(dimensions.values())
        score = sum(
            ((scores.get(key, 3) - 1) / 4) * weight
            for key, weight in dimensions.items()
        ) / max(total_weight, 0.001)
        reasons = sorted(
            dimensions,
            key=lambda key: scores.get(key, 3) * dimensions[key],
            reverse=True,
        )
        ranked_careers = {
            **career,
            "fit_score": score,
            "fit_reasons": [
                DIMENSION_LABELS[key] for key in reasons[:3] if key in DIMENSION_LABELS
            ],
        }
        ranked.append((score, ranked_careers))
    return [career for _, career in sorted(ranked, key=lambda item: item[0], reverse=True)]


def _session_for_user(user_id):
    session.clear()
    session["user_id"] = user_id
    session["csrf_token"] = secrets.token_urlsafe(32)
    session.permanent = True


def _valid_email(value):
    return bool(
        len(value) <= 254
        and re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value)
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("home"))
    if request.method == "POST":
        verify_csrf()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirm_password", "")
        if len(name) < 2 or len(name) > 60:
            flash("Your name must be between 2 and 60 characters.", "error")
        elif not _valid_email(email):
            flash("Enter a valid email address.", "error")
        elif len(password) < 10 or len(password) > 128:
            flash("Choose a password between 10 and 128 characters.", "error")
        elif password != confirmation:
            flash("The passwords do not match.", "error")
        else:
            database = get_db()
            try:
                database.execute("BEGIN IMMEDIATE")
                existing_user_count = database.execute(
                    "SELECT COUNT(*) AS count FROM users"
                ).fetchone()["count"]
                cursor = database.execute(
                    """INSERT INTO users (email, display_name, password_hash, theme, created_at)
                       VALUES (?, ?, ?, 'dark', ?)""",
                    (
                        email,
                        name,
                        generate_password_hash(password),
                        datetime.now().isoformat(timespec="seconds"),
                    ),
                )
                user_id = cursor.lastrowid
                database.execute(
                    "INSERT INTO user_progress (user_id) VALUES (?)", (user_id,)
                )
                if existing_user_count == 0:
                    migrate_legacy_data(database, user_id)
                database.commit()
            except sqlite3.IntegrityError:
                database.rollback()
                flash("An account with that email already exists. Try signing in instead.", "error")
            else:
                _session_for_user(user_id)
                flash(f"Welcome, {name}. Your private career journey is ready.", "success")
                return redirect(url_for("home"))
    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))
    if request.method == "POST":
        verify_csrf()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
        if (
            user is None
            or len(password) > 128
            or not check_password_hash(user["password_hash"], password)
        ):
            flash("Email or password is incorrect.", "error")
        else:
            _session_for_user(user["id"])
            return redirect(url_for("home"))
    return render_template("auth.html", mode="login")


@app.post("/logout")
@login_required
def logout():
    verify_csrf()
    session.clear()
    flash("You are signed out. Your progress is saved to your account.", "info")
    return redirect(url_for("login"))


@app.get("/")
@login_required
def home():
    user_id = session["user_id"]
    progress = current_progress() or {}
    career = career_by_id(selected_career_id(progress))
    tasks = daily_task_plan(user_id, career)
    completions = get_db().execute(
        "SELECT COUNT(*) AS count FROM task_completions WHERE user_id = ? AND completed_on = ?",
        (user_id, date.today().isoformat()),
    ).fetchone()["count"]
    completed = {
        row["task_id"]
        for row in get_db()
        .execute(
            "SELECT task_id FROM task_completions WHERE user_id = ? AND completed_on = ?",
            (user_id, date.today().isoformat()),
        )
        .fetchall()
    }
    return render_template(
        "home.html",
        progress=progress,
        career=career,
        completions=completions,
        assessment=latest_assessment(user_id),
        tasks=tasks,
        completed=completed,
        videos=video_recommendations(career),
    )


@app.route("/assessment", methods=["GET", "POST"])
@login_required
def assessment():
    if request.method == "POST":
        verify_csrf()
        totals = {}
        counts = {}
        for question in QUESTIONS:
            value = request.form.get(question["id"], type=int)
            if value not in range(1, 6):
                flash("Please answer every question before continuing.", "error")
                return render_template("assessment.html", questions=QUESTIONS), 400
            dimension = question["dimension"]
            totals[dimension] = totals.get(dimension, 0) + value
            counts[dimension] = counts.get(dimension, 0) + 1
        scores = {
            dimension: round(total / counts[dimension], 3)
            for dimension, total in totals.items()
        }
        matches = ranked_careers(scores)
        user_id = session["user_id"]
        database = get_db()
        database.execute(
            "INSERT INTO assessments (user_id, scores, created_at) VALUES (?, ?, ?)",
            (user_id, json.dumps(scores), datetime.now().isoformat(timespec="seconds")),
        )
        database.execute(
            "UPDATE user_progress SET selected_career = ? WHERE user_id = ?",
            (matches[0]["id"], user_id),
        )
        database.commit()
        return redirect(url_for("results"))
    return render_template("assessment.html", questions=QUESTIONS)


@app.get("/results")
@login_required
def results():
    user_id = session["user_id"]
    assessment_result = latest_assessment(user_id)
    if assessment_result is None:
        flash("Complete the assessment to see your career matches.", "info")
        return redirect(url_for("assessment"))
    return render_template(
        "results.html",
        matches=ranked_careers(assessment_result["scores"])[:6],
        assessment=assessment_result,
    )


@app.get("/careers")
@login_required
def careers():
    query = request.args.get("q", "").strip()[:100]
    category = request.args.get("category", "").strip()[:80]
    categories = sorted({career["category"] for career in CAREERS})
    filtered = CAREERS
    if category in categories:
        filtered = [career for career in filtered if career["category"] == category]
    else:
        category = ""
    if query:
        terms = query.casefold().split()
        filtered = [
            career
            for career in filtered
            if all(
                term in " ".join(
                    (career["title"], career["category"], career["description"])
                ).casefold()
                for term in terms
            )
        ]
    return render_template(
        "careers.html", careers=filtered, query=query, categories=categories, category=category
    )


@app.post("/careers/<career_id>/select")
@login_required
def select_career(career_id):
    verify_csrf()
    career = career_by_id(career_id)
    if career is None:
        abort(404)
    get_db().execute(
        "UPDATE user_progress SET selected_career = ? WHERE user_id = ?",
        (career_id, session["user_id"]),
    )
    get_db().commit()
    flash(f"{career['title']} is now your career direction to explore.", "success")
    return redirect(url_for("roadmap"))


@app.get("/roadmap")
@login_required
def roadmap():
    progress = current_progress() or {}
    career = career_by_id(selected_career_id(progress))
    if career is None:
        flash("Take the assessment to build your personalized roadmap.", "info")
        return redirect(url_for("assessment"))
    return render_template("roadmap.html", career=career)


@app.get("/tasks")
@login_required
def tasks():
    user_id = session["user_id"]
    progress = current_progress() or {}
    career = career_by_id(selected_career_id(progress))
    task_list = daily_task_plan(user_id, career)
    completed = {
        row["task_id"]
        for row in get_db()
        .execute(
            "SELECT task_id FROM task_completions WHERE user_id = ? AND completed_on = ?",
            (user_id, date.today().isoformat()),
        )
        .fetchall()
    }
    return render_template(
        "tasks.html",
        tasks=task_list,
        completed=completed,
        progress=progress,
        career=career,
        plan_date=date.today().isoformat(),
    )


@app.post("/tasks/<task_id>/complete")
@login_required
def complete_task(task_id):
    verify_csrf()
    progress = current_progress() or {}
    career = career_by_id(selected_career_id(progress))
    available_tasks = daily_task_plan(session["user_id"], career)
    if not any(task["id"] == task_id for task in available_tasks):
        abort(404)
    database = get_db()
    user_id = session["user_id"]
    today = date.today()
    today_key = today.isoformat()
    completion = database.execute(
        "SELECT 1 FROM task_completions WHERE user_id = ? AND task_id = ? AND completed_on = ?",
        (user_id, task_id, today_key),
    ).fetchone()
    if completion is None:
        progress = current_progress()
        last_active = date.fromisoformat(progress["last_active"]) if progress["last_active"] else None
        if last_active == today:
            streak = progress["streak"]
        elif last_active == today - timedelta(days=1):
            streak = progress["streak"] + 1
        else:
            streak = 1
        database.execute(
            "INSERT INTO task_completions (user_id, task_id, completed_on) VALUES (?, ?, ?)",
            (user_id, task_id, today_key),
        )
        database.execute(
            "UPDATE user_progress SET xp = xp + 20, streak = ?, last_active = ? WHERE user_id = ?",
            (streak, today_key, user_id),
        )
        database.commit()
        flash("Task complete! You earned 20 XP.", "success")
    else:
        flash("You already completed this task today.", "info")
    return redirect(url_for("tasks"))


@app.get("/api/day")
@login_required
def api_day():
    return jsonify({"date": date.today().isoformat()})


@app.get("/progress")
@login_required
def progress_page():
    user_id = session["user_id"]
    today = date.today()
    first_day = today - timedelta(days=6)
    rows = get_db().execute(
        """SELECT completed_on, COUNT(*) AS task_count
           FROM task_completions
           WHERE user_id = ? AND completed_on BETWEEN ? AND ?
           GROUP BY completed_on""",
        (user_id, first_day.isoformat(), today.isoformat()),
    ).fetchall()
    count_by_day = {row["completed_on"]: row["task_count"] for row in rows}
    largest_day = max(count_by_day.values(), default=1)
    week = [
        {
            "date": (first_day + timedelta(days=offset)).isoformat(),
            "label": (first_day + timedelta(days=offset)).strftime("%a"),
            "tasks": count_by_day.get(
                (first_day + timedelta(days=offset)).isoformat(), 0
            ),
            "bar": round(
                count_by_day.get(
                    (first_day + timedelta(days=offset)).isoformat(), 0
                )
                / largest_day
                * 100
            ),
        }
        for offset in range(7)
    ]
    weekly_tasks = sum(day["tasks"] for day in week)
    active_days = sum(day["tasks"] > 0 for day in week)
    total_tasks = get_db().execute(
        "SELECT COUNT(*) AS count FROM task_completions WHERE user_id = ?",
        (user_id,),
    ).fetchone()["count"]
    completed_task_types = get_db().execute(
        "SELECT COUNT(DISTINCT task_id) AS count FROM task_completions WHERE user_id = ?",
        (user_id,),
    ).fetchone()["count"]
    progress = current_progress() or {}
    career = career_by_id(selected_career_id(progress))
    return render_template(
        "progress.html",
        week=week,
        weekly_tasks=weekly_tasks,
        weekly_xp=weekly_tasks * 20,
        active_days=active_days,
        weekly_goal=12,
        total_tasks=total_tasks,
        completed_task_types=completed_task_types,
        progress=progress,
        career=career,
    )


@app.get("/profile")
@login_required
def profile():
    user_id = session["user_id"]
    progress = current_progress() or {}
    career = career_by_id(selected_career_id(progress))
    assessment_history = get_db().execute(
        "SELECT created_at FROM assessments WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user_id,),
    ).fetchall()
    return render_template(
        "profile.html",
        progress=progress,
        career=career,
        assessment_history=assessment_history,
        user=current_user(),
    )


@app.post("/profile/preferences")
@login_required
def update_preferences():
    verify_csrf()
    theme = request.form.get("theme", "")
    name = request.form.get("name", "").strip()
    if theme not in {"dark", "light"}:
        abort(400, description="Choose one of the available color themes.")
    if len(name) < 2 or len(name) > 60:
        flash("Your display name must be between 2 and 60 characters.", "error")
    else:
        get_db().execute(
            "UPDATE users SET display_name = ?, theme = ? WHERE id = ?",
            (name, theme, session["user_id"]),
        )
        get_db().commit()
        flash("Your profile preferences have been saved.", "success")
    return redirect(url_for("profile"))


@app.route("/mentor", methods=["GET", "POST"])
@login_required
def mentor():
    database = get_db()
    user_id = session["user_id"]
    progress = current_progress() or {}
    has_career = bool(selected_career_id(progress))
    if request.method == "POST":
        verify_csrf()
        message = request.form.get("message", "").strip()
        if not message or len(message) > 500:
            flash("Enter a message of up to 500 characters.", "error")
        else:
            career = career_by_id(selected_career_id(progress))
            reply = mentor_reply(message, career)
            intent = classify_intent(message)
            sources = json.dumps(
                [{"type": "career_catalog", "id": career["id"]}] if career else []
            )
            now = datetime.now().isoformat(timespec="seconds")
            database.executemany(
                """INSERT INTO mentor_messages
                   (user_id, role, message, sources, intent, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [
                    (user_id, "user", message, sources, intent, now),
                    (user_id, "mentor", reply, sources, intent, now),
                ],
            )
            database.commit()
        return redirect(url_for("mentor"))
    messages = database.execute(
        "SELECT role, message, created_at FROM mentor_messages WHERE user_id = ? ORDER BY id DESC LIMIT 30",
        (user_id,),
    ).fetchall()
    return render_template(
        "mentor.html", messages=list(reversed(messages)), has_career=has_career
    )


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5050")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
