from flask import Blueprint, request, render_template, make_response

bp = Blueprint("clickjacking", __name__, url_prefix="/lab/clickjacking")

# LEVEL 1: APPRENTICE (Tidak ada perlindungan anti-framing)
@bp.route("/apprentice/delete", methods=["GET", "POST"])
def apprentice_delete():
    message = None
    if request.method == "POST":
        message = "Akun Anda telah berhasil dihapus secara permanen!"
    
    # Render template tanpa header X-Frame-Options
    resp = make_response(render_template("labs/cj_apprentice.html", message=message))
    return resp

# LEVEL 2: PRACTITIONER (Perlindungan menggunakan Frame-Buster Script)
@bp.route("/practitioner/delete", methods=["GET", "POST"])
def practitioner_delete():
    message = None
    if request.method == "POST":
        message = "Akun Anda telah berhasil dihapus secara permanen!"
        
    resp = make_response(render_template("labs/cj_practitioner.html", message=message))
    return resp

# LEVEL 3: EXPERT (Pre-filled form dengan URL parameter)
@bp.route("/expert/transfer", methods=["GET", "POST"])
def expert_transfer():
    to_account = request.args.get("to", "user_default")
    message = None
    if request.method == "POST":
        message = f"Transfer dana sebesar $10,000 ke akun '{to_account}' BERHASIL!"
        
    resp = make_response(render_template("labs/cj_expert.html", to_account=to_account, message=message))
    return resp