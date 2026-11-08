# Career Compass

Career Compass is a Python/Flask career exploration website with individual accounts, a private progress database, a 38-question self-reflection assessment, a searchable career catalog, personalized starter roadmaps, detailed project-based tasks, XP and streak tracking, and a local machine-learning mentor prototype.

## Run locally

Python 3.10 or newer is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5050](http://127.0.0.1:5050) and create an account. Each account has its own assessments, chosen career, task completions, XP, streak, mentor chat, display name, and color theme. Dark mode is the default; the profile page can switch to light mode.

### Start automatically on Windows

The server normally stops when Windows shuts down. To have it start automatically each time you sign in to Windows, run `.\install_startup.ps1` once from PowerShell in this folder. This registers a per-user Task Scheduler job, starts the server in the background, and creates a `Career Compass.url` shortcut on your desktop. After restarting the PC and signing in, open the desktop shortcut (or visit [http://127.0.0.1:5050](http://127.0.0.1:5050)); no terminal command is needed. The supervisor restarts the server if it exits and writes diagnostic output to `logs\supervisor.log`, `logs\server-error.log`, and `logs\server.log`. To remove automatic startup, run `Unregister-ScheduledTask -TaskName 'Career Compass' -Confirm:$false` in PowerShell.

If `SECRET_KEY` is not set, the app creates a private `.career_compass_secret` file on first launch and reuses it so signed-in sessions survive server restarts. Keep this file private and do not delete it while you want existing sessions to remain valid. Successful registration and sign-in remember the browser on this device for up to one year; users can sign out from the profile or sidebar at any time. The SQLite database is created as `career_compass.db` beside `app.py`; set `DATABASE_PATH` to choose another location. Set `COOKIE_SECURE=1` when serving the site over HTTPS.

The mentor is deliberately local: a small multinomial Naive Bayes intent classifier learns from included example prompts and chooses guidance from the curated catalog. It is an educational prototype, not a generative AI, a professionally validated model, or a substitute for a qualified career adviser. Improve it with a responsibly sourced, reviewed, and representative dataset before relying on its predictions. User messages are not sent to an AI provider.

Career information and assessment guidance are locally curated snapshots; this version does not scrape or synchronize with job platforms. Before adding an external career source, use its permitted API or licensed dataset, review its terms, attribute content where required, and disclose any data shared. Career requirements and professional licensing vary by location. The assessment is exploratory and is not a validated psychometric test.

Daily task plans are locally generated and personalized from the selected career, assessment interests, recent task history, and the server's local calendar date. A new plan is created on the first request after midnight; an open tasks page checks for the date rollover and refreshes itself. This does not require an external AI service or a separate scheduler, but the web app must be running and the browser will check when it is open. Progress tracking summarizes saved task activity across the last seven days. The six career-learning links are YouTube search suggestions by difficulty, not endorsements or individually vetted videos.

On an original single-profile installation with no account records, the first registered account receives the saved progress and legacy tables are removed after the migration succeeds. If accounts already exist, their progress and retained legacy backup tables are left untouched; new accounts start with fresh progress instead. Back up `career_compass.db` before upgrading an installation with data.

This prototype is not production-ready for public deployment. Add email verification, password reset and rate limiting, secure secret management, backups, privacy/retention controls, a production WSGI server, and an independent security review before exposing it publicly.
