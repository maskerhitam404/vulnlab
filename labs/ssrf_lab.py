import requests
from flask import Blueprint, request, render_template, redirect

bp = Blueprint("ssrf_lab", __name__, url_prefix="/lab/ssrf")

# ==========================================
# MOCK ADMIN PANEL (Target Internal SSRF)
# ==========================================
@bp.route("/admin", methods=["GET"])
def admin_panel():
    return """
    <div style="padding:20px; font-family:sans-serif; border: 2px solid red; background-color: #fee2e2;">
        <h2>INTERNAL ADMIN PANEL</h2>
        <a href='/lab/ssrf/admin/delete?username=carlos' style="background: red; color: white; padding: 10px; text-decoration: none; border-radius: 5px;">Hapus Pengguna Carlos</a>
    </div>
    """

@bp.route("/admin/delete", methods=["GET"])
def admin_delete():
    username = request.args.get("username")
    if username == "carlos":
        return "SUCCESS: Pengguna 'carlos' berhasil dihapus secara permanen dari database internal!"
    return "ERROR: Pengguna tidak ditemukan."

# Mock API Stok Normal
@bp.route("/api/stock/<product_id>", methods=["GET"])
def dummy_stock(product_id):
    return f"Sistem Gudang: Sisa stok untuk produk ID {product_id} adalah 189 unit."

# ==========================================
# LEVEL 1: APPRENTICE (Tanpa Filter)
# ==========================================
@bp.route("/apprentice", methods=["GET"])
def apprentice_view():
    return render_template("labs/ssrf_apprentice.html")

@bp.route("/apprentice/stock", methods=["POST"])
def apprentice_stock():
    stock_api = request.form.get("stockApi")
    try:
        # VULNERABILITY: Melakukan HTTP Request ke URL sembarang tanpa validasi
        resp = requests.get(stock_api, timeout=3)
        return str(resp.text)
    except Exception as e:
        return f"Gagal menghubungi API stok: {str(e)}", 400

# ==========================================
# LEVEL 2: PRACTITIONER (Blacklist Filter)
# ==========================================
@bp.route("/practitioner", methods=["GET"])
def practitioner_view():
    return render_template("labs/ssrf_practitioner.html")

@bp.route("/practitioner/stock", methods=["POST"])
def practitioner_stock():
    stock_api = request.form.get("stockApi", "")
    
    # VULNERABILITY: Filter blacklist mudah dilewati menggunakan variasi IP (127.1)
    blocked_hosts = ["127.0.0.1", "localhost"]
    if any(blocked in stock_api for blocked in blocked_hosts):
        return "Akses Ditolak: Alamat host terdapat dalam daftar terlarang (Blacklist).", 403
        
    try:
        resp = requests.get(stock_api, timeout=3)
        return str(resp.text)
    except Exception as e:
        return f"Gagal menghubungi API stok: {str(e)}", 400

# ==========================================
# LEVEL 3: EXPERT (Whitelist & Open Redirect)
# ==========================================
@bp.route("/expert", methods=["GET"])
def expert_view():
    return render_template("labs/ssrf_expert.html")

@bp.route("/expert/stock", methods=["POST"])
def expert_stock():
    stock_api = request.form.get("stockApi", "")
    
    # Filter Whitelist: URL harus dimulai dengan path spesifik
    valid_prefix = "http://127.0.0.1:5000/lab/ssrf/expert/product"
    if not stock_api.startswith(valid_prefix):
        return "Akses Ditolak: URL API Stok harus berasal dari jaringan produk internal.", 403
        
    try:
        # VULNERABILITY: requests.get secara default mengikuti redirect.
        # Kombinasi ini dengan endpoint Open Redirect memungkinkan serangan SSRF.
        resp = requests.get(stock_api, timeout=3)
        return str(resp.text)
    except Exception as e:
        return f"Gagal menghubungi API stok: {str(e)}", 400

# Endpoint rentan Open Redirect yang berada di dalam lingkup Whitelist
@bp.route("/expert/product/next", methods=["GET"])
def expert_redirect():
    path = request.args.get("path")
    if path:
        return redirect(path)
    return "Parameter path tidak ditemukan.", 400