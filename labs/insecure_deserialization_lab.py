import base64
import json
import pickle
import yaml  # Membutuhkan: pip install pyyaml
from flask import Blueprint, request, render_template, make_response

bp = Blueprint("deserialization_lab", __name__, url_prefix="/lab/deserialization")

# ==========================================
# LEVEL 1: APPRENTICE (Base64 JSON Manipulation)
# ==========================================
@bp.route("/apprentice", methods=["GET"])
def apprentice_view():
    # Set cookie default jika tidak ada
    cookie_val = request.cookies.get("session_obj")
    
    if not cookie_val:
        # Default user object: {"username": "wiener", "is_admin": false}
        default_obj = {"username": "wiener", "is_admin": False}
        encoded_obj = base64.b64encode(json.dumps(default_obj).encode()).decode()
        
        resp = make_response(render_template("labs/deser_apprentice.html", is_admin=False))
        resp.set_cookie("session_obj", encoded_obj)
        return resp
        
    try:
        # VULNERABILITY: Mempercayai objek dari klien sepenuhnya tanpa cryptographic signature
        decoded_str = base64.b64decode(cookie_val).decode()
        user_obj = json.loads(decoded_str)
        is_admin = user_obj.get("is_admin", False)
        username = user_obj.get("username", "Unknown")
        
        return render_template("labs/deser_apprentice.html", is_admin=is_admin, username=username)
    except Exception:
        return "Cookie sesi rusak atau gagal di-decode.", 400


# ==========================================
# LEVEL 2: PRACTITIONER (Python Pickle RCE)
# ==========================================
@bp.route("/practitioner", methods=["GET", "POST"])
def practitioner_view():
    result = ""
    error = ""
    
    if request.method == "POST":
        token = request.form.get("token", "")
        try:
            # Decode token base64
            pickle_data = base64.b64decode(token)
            
            # VULNERABILITY: Melakukan unpickle pada data yang dikirim pengguna!
            # Ini akan memicu eksekusi __reduce__ secara otomatis.
            obj = pickle.loads(pickle_data)
            
            result = f"Token berhasil diproses. Objek: {str(obj)}"
        except Exception as e:
            error = f"Gagal memproses token (Namun RCE mungkin sudah dieksekusi di background!): {str(e)}"
            
    return render_template("labs/deser_practitioner.html", result=result, error=error)


# ==========================================
# LEVEL 3: EXPERT (YAML Deserialization RCE)
# ==========================================
@bp.route("/expert", methods=["GET", "POST"])
def expert_view():
    output_title = "Dashboard Default"
    output_color = "slate"
    error = ""
    
    # Default YAML Config
    yaml_config = """title: "Dashboard Kustom"
color: "blue"
"""

    if request.method == "POST":
        yaml_config = request.form.get("yaml_config", "")
        try:
            # VULNERABILITY: Menggunakan yaml.unsafe_load (atau yaml.load pada PyYAML versi lama)
            # Memungkinkan instansiasi objek kelas Python melalui tag !!python/object
            parsed_data = yaml.unsafe_load(yaml_config)
            
            if isinstance(parsed_data, dict):
                # Hasil RCE (seperti output subprocess) akan tersimpan di dalam dictionary ini
                output_title = str(parsed_data.get("title", output_title))
                output_color = str(parsed_data.get("color", output_color))
                
        except Exception as e:
            error = f"YAML Parsing Error: {str(e)}"
            
    return render_template("labs/deser_expert.html", 
                           yaml_config=yaml_config, 
                           title=output_title, 
                           color=output_color, 
                           error=error)