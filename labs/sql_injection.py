import sqlite3
import time
from flask import Blueprint, request, render_template, session

from database import get_db

bp = Blueprint("sql_injection", __name__, url_prefix="/lab/sql-injection")


@bp.route("/apprentice/login", methods=["GET", "POST"])
def apprentice_login():
    result = None
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        # VULNERABLE: string concatenation, no parameterization
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            row = conn.execute(query).fetchone()
            if row:
                result = f"Login berhasil sebagai '{row['username']}' (role: {row['role']}). Catatan rahasia: {row['secret_note']}"
            else:
                error = "Username atau password salah."
        except sqlite3.Error as e:
            error = f"SQL Error: {e}"
        conn.close()
    return render_template("labs/sqli_apprentice.html", result=result, error=error)


@bp.route("/practitioner/check")
def practitioner_check():
    item_id = request.args.get("id", "1")
    conn = get_db()
    query = f"SELECT * FROM products WHERE id = {item_id}"
    found = False
    try:
        row = conn.execute(query).fetchone()
        found = row is not None
    except sqlite3.Error:
        found = False
    conn.close()
    return render_template("labs/sqli_practitioner.html", item_id=item_id, found=found)


@bp.route("/expert/search")
def expert_search():
    q = request.args.get("q", "")
    conn = get_db()
    # VULNERABLE: string concatenation. Respons visual selalu sama (blind) -
    # satu-satunya sinyal adalah waktu, jika payload menyisipkan kondisi berat
    # seperti randomblob() saat kondisi TRUE.
    query = f"SELECT COUNT(*) as c FROM products WHERE name LIKE '%{q}%'"
    start = time.time()
    try:
        conn.execute(query).fetchall()
    except sqlite3.Error:
        pass
    elapsed = time.time() - start
    conn.close()
    # Respons selalu identik secara visual - hanya waktu yang berbeda
    return render_template("labs/sqli_expert.html", q=q, elapsed=round(elapsed, 3))
