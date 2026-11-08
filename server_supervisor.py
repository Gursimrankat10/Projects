import os
import subprocess
import time
import traceback
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", "5050"))
PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
LOGIN_URL = f"http://127.0.0.1:{PORT}/login"
LOG_DIR = PROJECT_ROOT / "logs"
SUPERVISOR_LOG = LOG_DIR / "supervisor.log"
SERVER_LOG = LOG_DIR / "server.log"
SERVER_ERROR_LOG = LOG_DIR / "server-error.log"


def write_log(message):
    LOG_DIR.mkdir(exist_ok=True)
    with SUPERVISOR_LOG.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")


def app_is_healthy():
    try:
        with urlopen(LOGIN_URL, timeout=3) as response:
            return response.status == 200 and b"Career Compass" in response.read()
    except (OSError, URLError):
        return False


def start_server():
    environment = os.environ.copy()
    environment["PORT"] = str(PORT)
    with SERVER_LOG.open("a", encoding="utf-8") as stdout_log, SERVER_ERROR_LOG.open(
        "a", encoding="utf-8"
    ) as stderr_log:
        return subprocess.Popen(
            [str(PYTHON), str(PROJECT_ROOT / "app.py")],
            cwd=PROJECT_ROOT,
            env=environment,
            stdout=stdout_log,
            stderr=stderr_log,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )


def supervise():
    server = None
    write_log(f"Supervisor started for {LOGIN_URL}.")
    while True:
        if server is not None and server.poll() is not None:
            write_log(f"Career Compass exited with status {server.returncode}; restarting.")
            server = None
        if server is None and not app_is_healthy():
            try:
                server = start_server()
                write_log(f"Started Career Compass (PID {server.pid}) at {LOGIN_URL}.")
            except OSError as error:
                write_log(f"Could not start Career Compass: {error}")
        time.sleep(5)


if __name__ == "__main__":
    try:
        supervise()
    except Exception:
        write_log(f"Supervisor stopped unexpectedly:\n{traceback.format_exc()}")
        raise
