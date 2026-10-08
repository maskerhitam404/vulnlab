import re
from flask import Blueprint, request, render_template, jsonify

bp = Blueprint("request_smuggling_lab", __name__, url_prefix="/lab/request-smuggling")

def simulate_hrs_parsing(raw_http, mode):
    """
    Simulator pemrosesan HTTP sederhana untuk mengilustrasikan logika CL.TE dan TE.CL.
    Bukan parser HTTP sungguhan, hanya dirancang untuk mencocokkan payload lab.
    """
    raw_http = raw_http.replace("\r\n", "\n").replace("\n", "\r\n") # Normalisasi CRLF
    
    try:
        # Pisahkan Header dan Body
        parts = raw_http.split("\r\n\r\n", 1)
        headers = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        
        # Ekstrak nilai CL dan deteksi keberadaan TE
        cl_match = re.search(r"Content-Length:\s*(\d+)", headers, re.IGNORECASE)
        cl_val = int(cl_match.group(1)) if cl_match else 0
        
        # Simulasi Obfuscation pada TE.TE (Expert)
        has_te_strict = bool(re.search(r"Transfer-Encoding:\s*chunked", headers, re.IGNORECASE))
        has_te_obfuscated = bool(re.search(r"Transfer-Encoding:\s*.*chunked", headers, re.IGNORECASE))
        
        fe_processed = ""
        be_processed = ""
        smuggled = ""

        if mode == "CL.TE":
            # FE menggunakan CL
            fe_processed = body[:cl_val]
            
            # BE menggunakan TE (Berhenti di chunk 0)
            chunk_end_idx = fe_processed.find("0\r\n")
            if chunk_end_idx != -1 and has_te_strict:
                be_processed = fe_processed[:chunk_end_idx + 3]
                smuggled = fe_processed[chunk_end_idx + 3:].lstrip()
            else:
                be_processed = fe_processed
                
        elif mode == "TE.CL":
            # FE menggunakan TE (Baca sampai chunk 0 atau habis)
            if has_te_strict:
                chunk_end_idx = body.find("0\r\n\r\n")
                if chunk_end_idx != -1:
                    fe_processed = body[:chunk_end_idx + 5]
                else:
                    fe_processed = body
            else:
                fe_processed = body[:cl_val]
                
            # BE menggunakan CL (Hanya membaca byte sejumlah CL)
            be_processed = fe_processed[:cl_val]
            if len(fe_processed) > cl_val:
                smuggled = fe_processed[cl_val:].lstrip()

        elif mode == "TE.TE":
            # FE menolak TE yang diobfuscasi, fallback ke CL
            if has_te_obfuscated and not has_te_strict:
                fe_processed = body[:cl_val]
            else:
                fe_processed = body # Simulasi normal
                
            # BE menerima TE yang diobfuscasi (Berhenti di chunk 0)
            if has_te_obfuscated:
                chunk_end_idx = fe_processed.find("0\r\n")
                if chunk_end_idx != -1:
                    be_processed = fe_processed[:chunk_end_idx + 3]
                    smuggled = fe_processed[chunk_end_idx + 3:].lstrip()
            else:
                be_processed = fe_processed

        is_success = bool(smuggled and ("GPOST" in smuggled or "POST" in smuggled))
        
        return {
            "success": is_success,
            "fe_view": fe_processed.strip(),
            "be_view": be_processed.strip(),
            "smuggled": smuggled.strip() if smuggled else "Tidak ada sisa request (buffer kosong)."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@bp.route("/apprentice", methods=["GET"])
def apprentice_view():
    return render_template("labs/reqsmug_apprentice.html")

@bp.route("/apprentice/simulate", methods=["POST"])
def apprentice_simulate():
    raw_http = request.form.get("raw_http", "")
    result = simulate_hrs_parsing(raw_http, "CL.TE")
    return jsonify(result)

@bp.route("/practitioner", methods=["GET"])
def practitioner_view():
    return render_template("labs/reqsmug_practitioner.html")

@bp.route("/practitioner/simulate", methods=["POST"])
def practitioner_simulate():
    raw_http = request.form.get("raw_http", "")
    result = simulate_hrs_parsing(raw_http, "TE.CL")
    return jsonify(result)

@bp.route("/expert", methods=["GET"])
def expert_view():
    return render_template("labs/reqsmug_expert.html")

@bp.route("/expert/simulate", methods=["POST"])
def expert_simulate():
    raw_http = request.form.get("raw_http", "")
    result = simulate_hrs_parsing(raw_http, "TE.TE")
    return jsonify(result)