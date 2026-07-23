import os
import re
from datetime import datetime

import psycopg2
from flask import Flask, render_template, request
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
csrf = CSRFProtect(app)

MIN_LENGTH = 1
MAX_LENGTH = 100
# Allow-list per OWASP Proactive Control C3: only characters a genuine
# search term needs. Anything else (<, >, ', ", ;, =, (, ) ... as used in
# XSS/SQLi payloads) is rejected outright.
ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9 ,.\-_]+$")


def is_valid_search_term(term):
    """Backend validation: length bounds + allow-list of characters."""
    if term is None:
        return False
    if not (MIN_LENGTH <= len(term) <= MAX_LENGTH):
        return False
    return bool(ALLOWED_PATTERN.fullmatch(term))


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "appdb"),
        user=os.environ.get("DB_USER", "appuser"),
        password=os.environ.get("DB_PASSWORD", "apppassword"),
    )


def log_search(term):
    conn = get_db_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                'INSERT INTO "2203778" (search_query, query_time) VALUES (%s, %s)',
                (term, datetime.now()),
            )
    finally:
        conn.close()


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", error=None)


@app.route("/search", methods=["POST"])
def search():
    term = request.form.get("search_term", "").strip()
    if not is_valid_search_term(term):
        return render_template("home.html", error="Invalid search term. Please try again.")
    log_search(term)
    return render_template("result.html", term=term)


if __name__ == "__main__":
    app.run(host=os.environ.get("FLASK_RUN_HOST", "127.0.0.1"), port=5000)
