from flask import Blueprint, request, render_template
from markupsafe import Markup

from database import get_db

bp = Blueprint("xss", __name__, url_prefix="/lab/xss")


@bp.route("/apprentice/search")
def apprentice_search():
    q = request.args.get("q", "")
    # VULNERABLE: dipantulkan langsung tanpa escaping (Markup melewati autoescape Jinja)
    unsafe_q = Markup(q) if q else ""
    return render_template("labs/xss_apprentice.html", q=unsafe_q, raw_q=q)


BLOCKED = ["<script"]


@bp.route("/practitioner/comment", methods=["GET", "POST"])
def practitioner_comment():
    error = None
    if request.method == "POST":
        author = request.form.get("author", "anonymous")
        body = request.form.get("body", "")
        # VULNERABLE: filter blacklist lemah, hanya cek '<script' persis (case sensitive)
        if "<script" in body:
            error = "Komentar ditolak: tag script terdeteksi."
        else:
            conn = get_db()
            conn.execute(
                "INSERT INTO comments (lab_scope, author, body) VALUES (?, ?, ?)",
                ("xss-practitioner", author, body),
            )
            conn.commit()
            conn.close()

    conn = get_db()
    comments = conn.execute(
        "SELECT * FROM comments WHERE lab_scope = 'xss-practitioner' ORDER BY id DESC"
    ).fetchall()
    conn.close()
    # Komentar dirender dengan Markup (unsafe) agar payload stored benar-benar tereksekusi
    unsafe_comments = [
        {"author": c["author"], "body": Markup(c["body"]), "id": c["id"]} for c in comments
    ]
    return render_template("labs/xss_practitioner.html", comments=unsafe_comments, error=error)


@bp.route("/expert/welcome")
def expert_welcome():
    # DOM-based: server tidak pernah melihat payload, semua terjadi di JS lewat location.hash
    return render_template("labs/xss_expert.html")
