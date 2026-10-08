from flask import Blueprint, request, render_template_string, render_template

bp = Blueprint("ssti_lab", __name__, url_prefix="/lab/ssti")

# ==========================================
# LEVEL 1: APPRENTICE (Basic SSTI)
# ==========================================
@bp.route("/apprentice", methods=["GET", "POST"])
def apprentice():
    # Mengambil input dari pengguna, default 'Pengguna'
    name_input = request.args.get("name", "Pengguna")
    
    try:
        # VULNERABILITY: Mengeksekusi string yang terkontaminasi input pengguna
        # sebagai template Jinja2 secara langsung.
        rendered_name = render_template_string(name_input)
    except Exception as e:
        rendered_name = "Error rendering template"
        
    return render_template("labs/ssti_apprentice.html", name=rendered_name, raw_input=name_input)


# ==========================================
# LEVEL 2: PRACTITIONER (Blacklist Filtered SSTI)
# ==========================================
@bp.route("/practitioner", methods=["GET", "POST"])
def practitioner():
    name_input = request.args.get("name", "Pengguna")
    
    # FILTER: Memblokir karakter underscore yang sering dipakai untuk RCE
    if "_" in name_input:
        rendered_name = "Aksi diblokir: Karakter '_' tidak diizinkan pada platform ini."
    else:
        try:
            rendered_name = render_template_string(name_input)
        except Exception:
            rendered_name = "Error rendering template"
            
    return render_template("labs/ssti_practitioner.html", name=rendered_name, raw_input=name_input)


# ==========================================
# LEVEL 3: EXPERT (Blind SSTI)
# ==========================================
@bp.route("/expert", methods=["GET", "POST"])
def expert():
    email_input = request.args.get("email", "")
    message = ""
    
    if email_input:
        try:
            # VULNERABILITY (BLIND): Template dieksekusi oleh server
            # namun hasil evaluasinya tidak pernah dilempar kembali ke antarmuka pengguna (dibuang).
            _ = render_template_string(f"Pendaftaran email untuk {email_input}")
            message = "Terima kasih! Kami akan segera menghubungi Anda."
        except Exception:
            # Tetap menampilkan pesan sukses agar penyerang kesulitan membedakan status
            message = "Terima kasih! Kami akan segera menghubungi Anda."
            
    return render_template("labs/ssti_expert.html", message=message, raw_input=email_input)