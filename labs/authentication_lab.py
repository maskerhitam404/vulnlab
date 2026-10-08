from flask import Blueprint, request, render_template, session, redirect, url_for

bp = Blueprint("authentication_lab", __name__, url_prefix="/lab/authentication")

# Database Dummy
USERS = {
    "wiener": "peter",
    "carlos": "qwerty",
    "admin": "admin123"
}

# ==========================================
# LEVEL 1: APPRENTICE (Enumeration & Brute Force)
# ==========================================
@bp.route("/apprentice/login", methods=["GET", "POST"])
def apprentice_login():
    error_msg = ""
    success_msg = ""
    
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        # VULNERABILITY: Respons error yang berbeda (Username enumeration)
        if username not in USERS:
            error_msg = "Username tidak ditemukan."
        elif USERS[username] != password:
            error_msg = "Password salah."
        else:
            success_msg = f"Login Berhasil! Selamat datang, {username}."
            
    return render_template("labs/auth_apprentice.html", error_msg=error_msg, success_msg=success_msg)


# ==========================================
# LEVEL 2: PRACTITIONER (Bypass IP Rate Limiting)
# ==========================================
# Penyimpanan sementara untuk menghitung percobaan (reset saat restart server)
failed_attempts = {}

@bp.route("/practitioner/login", methods=["GET", "POST"])
def practitioner_login():
    error_msg = ""
    success_msg = ""
    
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        # VULNERABILITY: Percaya pada header X-Forwarded-For untuk Rate Limiting
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        
        if failed_attempts.get(client_ip, 0) >= 3:
            return "Akses Ditolak: Terlalu banyak percobaan login yang gagal dari IP ini.", 429
            
        if username == "carlos" and password == "qwerty":
            success_msg = "Login Berhasil! Anda menembus blokir IP."
            failed_attempts[client_ip] = 0 # Reset on success
        else:
            error_msg = "Username atau password salah."
            failed_attempts[client_ip] = failed_attempts.get(client_ip, 0) + 1
            
    return render_template("labs/auth_practitioner.html", error_msg=error_msg, success_msg=success_msg)


# ==========================================
# LEVEL 3: EXPERT (Flawed 2FA)
# ==========================================
@bp.route("/expert/login", methods=["GET", "POST"])
def expert_login():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        if username == "carlos" and password == "qwerty":
            # Berhasil login tahap 1, inisiasi sesi 2FA
            session["mfa_pending"] = username
            return redirect(url_for("authentication_lab.expert_2fa"))
        else:
            error_msg = "Username atau password salah."
            
    return render_template("labs/auth_expert_login.html", error_msg=error_msg)


@bp.route("/expert/2fa", methods=["GET", "POST"])
def expert_2fa():
    # Pastikan pengguna sudah melewati tahap 1
    if "mfa_pending" not in session:
        return redirect(url_for("authentication_lab.expert_login"))
        
    error_msg = ""
    success_msg = ""
    
    # Kode PIN 2FA yang harus ditebak (Hardcoded untuk keperluan lab)
    # Dalam skenario asli, ini di-generate secara acak.
    VALID_PIN = "4812"
    
    if request.method == "POST":
        mfa_code = request.form.get("mfa-code", "")
        
        # VULNERABILITY: Tidak ada Rate Limiting sama sekali di endpoint ini.
        # Penyerang bisa melakukan brute force dari 0000 - 9999.
        if mfa_code == VALID_PIN:
            user = session.pop("mfa_pending")
            success_msg = f"Autentikasi 2FA Berhasil! Anda kini login sebagai: {user}."
        else:
            error_msg = "Kode verifikasi salah."
            
    return render_template("labs/auth_expert_2fa.html", error_msg=error_msg, success_msg=success_msg)