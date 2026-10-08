import uuid
from flask import Blueprint, request, render_template, session

bp = Blueprint("csrf", __name__, url_prefix="/lab/csrf")

@bp.route("/apprentice/email", methods=["GET", "POST"])
def apprentice_email():
    if "apprentice_email" not in session:
        session["apprentice_email"] = "user@ifsec.local"
        
    message = None
    if request.method == "POST":
        new_email = request.form.get("email")
        if new_email:
            session["apprentice_email"] = new_email
            message = "Email berhasil diperbarui!"
            
    return render_template("labs/csrf_apprentice.html", email=session["apprentice_email"], message=message)


@bp.route("/practitioner/email", methods=["GET", "POST"])
def practitioner_email():
    if "practitioner_email" not in session:
        session["practitioner_email"] = "user@ifsec.local"
        
    if "pract_csrf" not in session:
        session["pract_csrf"] = uuid.uuid4().hex
        
    message = None
    error = None
    if request.method == "POST":
        new_email = request.form.get("email")
        submitted_token = request.form.get("csrf")
        
        # Validasi cacat: hanya mengecek jika parameter csrf dikirimkan
        if submitted_token is not None:
            if submitted_token != session["pract_csrf"]:
                error = "Aksi ditolak: CSRF token tidak valid!"
            else:
                session["practitioner_email"] = new_email
                message = "Email berhasil diperbarui!"
        else:
            session["practitioner_email"] = new_email
            message = "Email berhasil diperbarui! (Parameter Token Diabaikan)"

    return render_template("labs/csrf_practitioner.html", 
                           email=session["practitioner_email"], 
                           message=message, 
                           error=error, 
                           csrf_token=session["pract_csrf"])


@bp.route("/expert/email", methods=["GET", "POST"])
def expert_email():
    if "expert_email" not in session:
        session["expert_email"] = "user@ifsec.local"
        
    message = None
    error = None
    
    if request.method == "POST":
        new_email = request.form.get("email")
        referer = request.headers.get("Referer")
        host = request.host
        
        # Validasi cacat: bypass terjadi jika header Referer sama sekali tidak ada (None)
        if referer:
            if host not in referer:
                error = "Aksi ditolak: Header Referer tidak valid!"
            else:
                session["expert_email"] = new_email
                message = "Email berhasil diperbarui!"
        else:
            session["expert_email"] = new_email
            message = "Email berhasil diperbarui! (Header Referer Kosong)"

    return render_template("labs/csrf_expert.html", email=session["expert_email"], message=message, error=error)