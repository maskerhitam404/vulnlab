from flask import Blueprint, request, render_template

bp = Blueprint("dom_based", __name__, url_prefix="/lab/dom-based")

# LEVEL 1: APPRENTICE (DOM XSS via innerHTML)
@bp.route("/apprentice/search", methods=["GET"])
def apprentice_search():
    # Perhatikan: Backend TIDAK memproses parameter 'q' untuk mencari data.
    # Semua logika diproses di sisi klien (browser) oleh file HTML.
    return render_template("labs/dom_apprentice.html")

# LEVEL 2: PRACTITIONER (DOM XSS via eval() and location.hash)
@bp.route("/practitioner/theme", methods=["GET"])
def practitioner_theme():
    # Fragment URL (#) tidak pernah dikirim ke server. 
    # Flask hanya merender halaman kosongan.
    return render_template("labs/dom_practitioner.html")

# LEVEL 3: EXPERT (DOM Open Redirection via javascript: pseudo-protocol)
@bp.route("/expert/redirect", methods=["GET"])
def expert_redirect():
    # Mengirim parameter URL ke klien, walau JS di klien yang membacanya.
    return render_template("labs/dom_expert.html")