from flask import Blueprint, request, render_template, jsonify
from lxml import etree  # HARUS di-install via pip (pip install lxml)

bp = Blueprint("xxe_lab", __name__, url_prefix="/lab/xxe")

# ==========================================
# LEVEL 1: APPRENTICE (In-Band XXE)
# ==========================================
@bp.route("/apprentice", methods=["GET"])
def apprentice_view():
    return render_template("labs/xxe_apprentice.html")

@bp.route("/apprentice/stock", methods=["POST"])
def apprentice_stock():
    xml_data = request.data
    try:
        # VULNERABILITY: resolve_entities=True mengizinkan pemrosesan external entity!
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        root = etree.fromstring(xml_data, parser)
        
        product_id = root.findtext("productId")
        if not product_id:
            return "Error: Elemen <productId> tidak ditemukan dalam XML.", 400
            
        return f"Stok untuk produk {product_id} adalah 42 unit."
    except Exception as e:
        return f"XML Parsing Error: {str(e)}", 400


# ==========================================
# LEVEL 2: PRACTITIONER (XXE to SSRF)
# ==========================================
@bp.route("/practitioner", methods=["GET"])
def practitioner_view():
    return render_template("labs/xxe_practitioner.html")

@bp.route("/practitioner/stock", methods=["POST"])
def practitioner_stock():
    xml_data = request.data
    try:
        # VULNERABILITY: Mengizinkan pemrosesan entity jaringan (SSRF)
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        root = etree.fromstring(xml_data, parser)
        
        product_id = root.findtext("productId")
        return f"Sistem internal mengkonfirmasi stok untuk: {product_id} = 15 unit."
    except Exception as e:
        return f"XML Parsing Error: {str(e)}", 400

# Endpoint rahasia simulasi SSRF target (AWS Metadata dsb)
@bp.route("/internal/secret", methods=["GET"])
def internal_secret():
    # Dalam skenario asli, ini mungkin dibatasi IP-nya
    return "RAHASIA_INTERNAL: Kunci master API adalah 'IFSEC-SUPER-SECRET-99'."


# ==========================================
# LEVEL 3: EXPERT (XInclude)
# ==========================================
@bp.route("/expert", methods=["GET"])
def expert_view():
    return render_template("labs/xxe_expert.html")

@bp.route("/expert/stock", methods=["POST"])
def expert_stock():
    # Menerima form biasa, bukan XML mentah
    product_id = request.form.get("productId", "")
    
    # Aplikasi backend menyisipkan input langsung ke XML internal
    xml_string = f"""<?xml version="1.0" encoding="UTF-8"?>
    <stockCheck>
        <productId>{product_id}</productId>
    </stockCheck>
    """
    
    try:
        parser = etree.XMLParser(resolve_entities=True)
        root = etree.fromstring(xml_string.encode('utf-8'), parser)
        
        # VULNERABILITY: Backend menjalankan fungsi xinclude() pada input!
        root.xinclude() 
        
        val = root.findtext('productId')
        return f"Cek stok berhasil. Sisa barang untuk ID {val} adalah 8 unit."
    except Exception as e:
        return f"Internal XML Error: {str(e)}", 400