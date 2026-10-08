import uuid
from flask import Blueprint, request, render_template, session, jsonify, make_response

bp = Blueprint("cors_lab", __name__, url_prefix="/lab/cors")

# Helper untuk inisiasi API Key
def init_api_keys():
    if "cors_apprentice_key" not in session:
        session["cors_apprentice_key"] = f"IFSEC-APP-{uuid.uuid4().hex[:8]}"
    if "cors_practitioner_key" not in session:
        session["cors_practitioner_key"] = f"IFSEC-PRC-{uuid.uuid4().hex[:8]}"
    if "cors_expert_key" not in session:
        session["cors_expert_key"] = f"IFSEC-EXP-{uuid.uuid4().hex[:8]}"

# ==========================================
# LEVEL 1: APPRENTICE (Memantulkan semua Origin)
# ==========================================
@bp.route("/apprentice", methods=["GET"])
def apprentice_view():
    init_api_keys()
    return render_template("labs/cors_apprentice.html", apikey=session["cors_apprentice_key"])

@bp.route("/apprentice/api/account", methods=["GET"])
def apprentice_api():
    init_api_keys()
    data = {
        "status": "success",
        "username": "administrator",
        "email": "admin@ifsec.local",
        "apikey": session["cors_apprentice_key"]
    }
    resp = make_response(jsonify(data))
    
    # VULNERABILITY: Membaca Origin dan langsung menyalinnya ke header ACAO
    origin = request.headers.get("Origin")
    if origin:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        
    return resp

# ==========================================
# LEVEL 2: PRACTITIONER (Mengizinkan Null Origin)
# ==========================================
@bp.route("/practitioner", methods=["GET"])
def practitioner_view():
    init_api_keys()
    return render_template("labs/cors_practitioner.html", apikey=session["cors_practitioner_key"])

@bp.route("/practitioner/api/account", methods=["GET"])
def practitioner_api():
    init_api_keys()
    data = {
        "status": "success",
        "username": "administrator",
        "email": "admin@ifsec.local",
        "apikey": session["cors_practitioner_key"]
    }
    resp = make_response(jsonify(data))
    
    origin = request.headers.get("Origin")
    # VULNERABILITY: Mengizinkan secara eksplisit origin 'null'
    if origin == "null":
        resp.headers["Access-Control-Allow-Origin"] = "null"
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        
    return resp

# ==========================================
# LEVEL 3: EXPERT (Validasi Regex/Pola Lemah)
# ==========================================
@bp.route("/expert", methods=["GET"])
def expert_view():
    init_api_keys()
    return render_template("labs/cors_expert.html", apikey=session["cors_expert_key"])

@bp.route("/expert/api/account", methods=["GET"])
def expert_api():
    init_api_keys()
    data = {
        "status": "success",
        "username": "administrator",
        "email": "admin@ifsec.local",
        "apikey": session["cors_expert_key"]
    }
    resp = make_response(jsonify(data))
    
    origin = request.headers.get("Origin")
    # VULNERABILITY: Logika startswith yang lemah. 
    # Bisa di-bypass dengan http://127.0.0.1:5000.situs-penyerang.com
    if origin and origin.startswith("http://127.0.0.1:5000"):
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        
    return resp