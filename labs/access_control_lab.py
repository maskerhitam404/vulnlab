from flask import Blueprint, request, render_template, make_response, redirect, url_for

bp = Blueprint("access_control_lab", __name__, url_prefix="/lab/access-control")

# ==========================================
# LEVEL 1: APPRENTICE (Unprotected Admin)
# ==========================================
@bp.route("/apprentice", methods=["GET"])
def apprentice_view():
    return render_template("labs/ac_apprentice.html")

@bp.route("/apprentice/admin", methods=["GET"])
def apprentice_admin():
    # VULNERABILITY: Tidak ada pengecekan sesi atau peran admin sama sekali!
    # Siapapun yang mengetahui URL ini bisa mengaksesnya.
    action = request.args.get("action")
    message = ""
    if action == "delete_carlos":
        message = "BERHASIL: Pengguna 'carlos' telah dihapus dari sistem."
        
    return render_template("labs/ac_apprentice_admin.html", message=message)


# ==========================================
# LEVEL 2: PRACTITIONER (IDOR)
# ==========================================
# Database statis tiruan
TICKETS_DB = {
    "1": {"owner": "wiener", "title": "Bantuan Reset Password", "body": "Halo, saya lupa password saya. Tolong bantu reset."},
    "2": {"owner": "carlos", "title": "Laporan Bug Kritis", "body": "RAHASIA: Saya menemukan celah keamanan di server utama. Token AWS: AKIAIOSFODNN7EXAMPLE"},
    "3": {"owner": "administrator", "title": "Update Server", "body": "Jadwal maintenance server dipindah ke jam 2 pagi."}
}

@bp.route("/practitioner", methods=["GET"])
def practitioner_view():
    return render_template("labs/ac_practitioner.html")

@bp.route("/practitioner/ticket", methods=["GET"])
def practitioner_ticket():
    ticket_id = request.args.get("id")
    
    if not ticket_id:
        return redirect(url_for("access_control_lab.practitioner_view"))
        
    # VULNERABILITY: IDOR. Aplikasi mengambil data berdasarkan ID
    # tanpa memeriksa apakah 'owner' dari tiket tersebut adalah pengguna yang sedang login.
    ticket_data = TICKETS_DB.get(ticket_id)
    
    if ticket_data:
        return render_template("labs/ac_practitioner_ticket.html", ticket=ticket_data, ticket_id=ticket_id)
    else:
        return "Tiket tidak ditemukan.", 404


# ==========================================
# LEVEL 3: EXPERT (Cookie Privilege Escalation)
# ==========================================
@bp.route("/expert", methods=["GET"])
def expert_view():
    resp = make_response(render_template("labs/ac_expert.html"))
    # Menetapkan cookie default dengan role user
    if not request.cookies.get("user_role"):
        resp.set_cookie("user_role", "user")
    return resp

@bp.route("/expert/admin", methods=["GET"])
def expert_admin():
    # Mengambil nilai cookie, default ke 'guest' jika tidak ada
    role = request.cookies.get("user_role", "guest")
    
    if role == "admin":
        # Jika berhasil manipulasi cookie menjadi admin
        return render_template("labs/ac_expert_admin.html")
    else:
        # Jika bukan admin, tolak akses menggunakan file HTML yang SAMA, 
        # namun kita mengirimkan variabel current_role agar Jinja2 memunculkan pesan error.
        return render_template("labs/ac_expert_admin.html", current_role=role)