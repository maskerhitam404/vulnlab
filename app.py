import os
from flask import Flask, render_template, abort, jsonify

from data.catalog import CATEGORIES, CATEGORY_MAP, LEVELS, LEVEL_META, get_lab
from database import init_db, DB_PATH

from labs.sql_injection import bp as sqli_bp
from labs.xss import bp as xss_bp
from labs.command_injection import bp as cmdi_bp
from labs.path_traversal import bp as pathtrav_bp
from labs.sql_injection import bp as sqli_bp
from labs.xss import bp as xss_bp
from labs.command_injection import bp as cmdi_bp
from labs.path_traversal import bp as pathtrav_bp
from labs.csrf import bp as csrf_bp  # <--- TAMBAHKAN INI
from labs.clickjacking import bp as cj_bp
from labs.dom_based import bp as dom_bp
from labs.cors_lab import bp as cors_bp
from labs.xxe_lab import bp as xxe_bp
from labs.ssrf_lab import bp as ssrf_bp
from labs.request_smuggling_lab import bp as reqsmug_bp
from labs.ssti_lab import bp as ssti_bp
from labs.access_control_lab import bp as ac_bp
from labs.authentication_lab import bp as auth_bp
from labs.insecure_deserialization_lab import bp as deser_bp
from labs.file_upload_lab import bp as upload_bp
from data.catalog import CATEGORIES

app = Flask(__name__)
app.secret_key = "lab-secret-key-not-for-production"

app.register_blueprint(sqli_bp)
app.register_blueprint(xss_bp)
app.register_blueprint(cmdi_bp)
app.register_blueprint(pathtrav_bp)
app.register_blueprint(csrf_bp)      # <--- TAMBAHKAN INI
app.register_blueprint(cj_bp)
app.register_blueprint(dom_bp)
app.register_blueprint(cors_bp)
app.register_blueprint(xxe_bp)
app.register_blueprint(ssrf_bp)
app.register_blueprint(reqsmug_bp)
app.register_blueprint(ssti_bp)
app.register_blueprint(ac_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(deser_bp)
app.register_blueprint(upload_bp)

# Peta slug lab -> endpoint Flask, dipakai tombol "Akses Lab"
LAB_ROUTE_MAP = {
    ("sql-injection", "apprentice"): "sql_injection.apprentice_login",
    ("sql-injection", "practitioner"): "sql_injection.practitioner_check",
    ("sql-injection", "expert"): "sql_injection.expert_search",
    ("xss", "apprentice"): "xss.apprentice_search",
    ("xss", "practitioner"): "xss.practitioner_comment",
    ("xss", "expert"): "xss.expert_welcome",
    ("command-injection", "apprentice"): "command_injection.apprentice_ping",
    ("command-injection", "practitioner"): "command_injection.practitioner_notify",
    ("command-injection", "expert"): "command_injection.expert_lookup",
    ("path-traversal", "apprentice"): "path_traversal.apprentice_image",
    ("path-traversal", "practitioner"): "path_traversal.practitioner_download",
    ("path-traversal", "expert"): "path_traversal.expert_thumbnail",
    ("csrf", "apprentice"): "csrf.apprentice_email",
    ("csrf", "practitioner"): "csrf.practitioner_email",
    ("csrf", "expert"): "csrf.expert_email",
    ("clickjacking", "apprentice"): "clickjacking.apprentice_delete",
    ("clickjacking", "practitioner"): "clickjacking.practitioner_delete",
    ("clickjacking", "expert"): "clickjacking.expert_transfer",
    ("dom-based", "apprentice"): "dom_based.apprentice_search",
    ("dom-based", "practitioner"): "dom_based.practitioner_theme",
    ("dom-based", "expert"): "dom_based.expert_redirect",
    ("cors", "apprentice"): "cors_lab.apprentice_view",
    ("cors", "practitioner"): "cors_lab.practitioner_view",
    ("cors", "expert"): "cors_lab.expert_view",
    ("xxe", "apprentice"): "xxe_lab.apprentice_view",
    ("xxe", "practitioner"): "xxe_lab.practitioner_view",
    ("xxe", "expert"): "xxe_lab.expert_view",
    ("ssrf", "apprentice"): "ssrf_lab.apprentice_view",
    ("ssrf", "practitioner"): "ssrf_lab.practitioner_view",
    ("ssrf", "expert"): "ssrf_lab.expert_view",
    ("request-smuggling", "apprentice"): "request_smuggling_lab.apprentice_view",
    ("request-smuggling", "practitioner"): "request_smuggling_lab.practitioner_view",
    ("request-smuggling", "expert"): "request_smuggling_lab.expert_view",
    ("ssti", "apprentice"): "ssti_lab.apprentice",
    ("ssti", "practitioner"): "ssti_lab.practitioner",
    ("ssti", "expert"): "ssti_lab.expert",
    ("access-control", "apprentice"): "access_control_lab.apprentice_view",
    ("access-control", "practitioner"): "access_control_lab.practitioner_view",
    ("access-control", "expert"): "access_control_lab.expert_view",
    ("authentication", "apprentice"): "authentication_lab.apprentice_login",
    ("authentication", "practitioner"): "authentication_lab.practitioner_login",
    ("authentication", "expert"): "authentication_lab.expert_login",
    ("deserialization", "apprentice"): "deserialization_lab.apprentice_view",
    ("deserialization", "practitioner"): "deserialization_lab.practitioner_view",
    ("deserialization", "expert"): "deserialization_lab.expert_view",
    ("file-upload", "apprentice"): "file_upload_lab.apprentice",
    ("file-upload", "practitioner"): "file_upload_lab.practitioner",
    ("file-upload", "expert"): "file_upload_lab.expert",
}


@app.context_processor
def inject_globals():
    return dict(CATEGORIES=CATEGORIES, LEVELS=LEVELS, LEVEL_META=LEVEL_META)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/category/<slug>")
def category(slug):
    # Mengamankan format slug agar cocok dengan dictionary/map di backend
    safe_slug = slug.strip().lower()
    
    # Mencari slug dengan metode case-insensitive
    cat = None
    for key, value in CATEGORY_MAP.items():
        if key.strip().lower() == safe_slug:
            cat = value
            break
            
    if not cat:
        # Jika gagal, akan memicu route 404
        abort(404)
        
    return render_template("category.html", cat=cat)

@app.route("/category/<slug>/<level>")
def tutorial(slug, level):
    cat = CATEGORY_MAP.get(slug)
    if not cat or level not in LEVELS:
        abort(404)
    lab = get_lab(slug, level)
    lab_endpoint = LAB_ROUTE_MAP.get((slug, level))
    return render_template(
        "tutorial.html",
        cat=cat,
        level=level,
        level_meta=LEVEL_META[level],
        lab=lab,
        lab_endpoint=lab_endpoint,
        implemented=cat["implemented"],
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
