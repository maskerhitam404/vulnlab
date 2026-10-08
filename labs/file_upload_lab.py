from flask import Blueprint, request, render_template

bp = Blueprint("file_upload_lab", __name__, url_prefix="/lab/file-upload")

# Fungsi helper untuk mensimulasikan eksekusi web shell secara aman (tanpa mengeksekusi kode sungguhan)
def simulate_execution(filename, content):
    executable_exts = ('.php', '.php3', '.php4', '.php5', '.phtml', '.phar')
    if filename.lower().endswith(executable_exts):
        if b'<?php' in content or b'system' in content or b'echo' in content:
            return True, "SIMULASI RCE BERHASIL: File web shell tereksekusi oleh server virtual!"
        return True, "File terdeteksi sebagai executable, namun payload tidak dikenali."
    return False, "File berhasil diunggah dan disimpan sebagai statis."

# ==========================================
# LEVEL 1: APPRENTICE (Unrestricted Upload)
# ==========================================
@bp.route("/apprentice", methods=["GET", "POST"])
def apprentice():
    message = ""
    status = ""
    
    if request.method == "POST":
        if 'avatar' not in request.files:
            message = "Tidak ada file yang dipilih."
            status = "error"
        else:
            file = request.files['avatar']
            if file.filename == '':
                message = "Tidak ada file yang dipilih."
                status = "error"
            else:
                # VULNERABILITY: Tidak ada validasi nama, tipe, atau isi file
                content = file.read()
                is_executed, msg = simulate_execution(file.filename, content)
                message = msg
                status = "success" if is_executed else "info"

    return render_template("labs/upload_apprentice.html", message=message, status=status)


# ==========================================
# LEVEL 2: PRACTITIONER (Content-Type Bypass)
# ==========================================
@bp.route("/practitioner", methods=["GET", "POST"])
def practitioner():
    message = ""
    status = ""
    
    if request.method == "POST":
        if 'avatar' not in request.files:
            message = "Tidak ada file yang dipilih."
            status = "error"
        else:
            file = request.files['avatar']
            if file.filename != '':
                # VULNERABILITY: Hanya memvalidasi MimeType/Content-Type dari request klien
                content_type = file.mimetype
                if content_type not in ['image/jpeg', 'image/png']:
                    message = f"Gagal: Hanya file gambar (image/jpeg, image/png) yang diizinkan. Tipe Anda: {content_type}"
                    status = "error"
                else:
                    content = file.read()
                    is_executed, msg = simulate_execution(file.filename, content)
                    message = msg
                    status = "success" if is_executed else "info"

    return render_template("labs/upload_practitioner.html", message=message, status=status)


# ==========================================
# LEVEL 3: EXPERT (Blacklist Bypass)
# ==========================================
@bp.route("/expert", methods=["GET", "POST"])
def expert():
    message = ""
    status = ""
    
    if request.method == "POST":
        if 'avatar' not in request.files:
            message = "Tidak ada file yang dipilih."
            status = "error"
        else:
            file = request.files['avatar']
            if file.filename != '':
                filename = file.filename.lower()
                
                # FILTER: Blacklist ekstensi tertentu
                if filename.endswith('.php'):
                    message = "Gagal: Ekstensi .php diblokir demi keamanan."
                    status = "error"
                else:
                    # VULNERABILITY: Ekstensi alternatif (.php5, .phtml) tidak diblokir
                    content = file.read()
                    is_executed, msg = simulate_execution(file.filename, content)
                    message = msg
                    status = "success" if is_executed else "info"

    return render_template("labs/upload_expert.html", message=message, status=status)