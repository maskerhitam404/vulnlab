import os
import urllib.parse
from flask import Blueprint, request, render_template

bp = Blueprint("path_traversal", __name__, url_prefix="/lab/path-traversal")

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lab_files")


@bp.route("/apprentice/image")
def apprentice_image():
    filename = request.args.get("filename", "")
    content = None
    error = None
    if filename:
        # VULNERABLE: tidak ada normalisasi/validasi sama sekali
        path = os.path.join(BASE_DIR, filename)
        try:
            with open(path, "r", errors="replace") as f:
                content = f.read(4000)
        except Exception as e:
            error = str(e)
    return render_template("labs/pathtrav_apprentice.html", filename=filename, content=content, error=error)


@bp.route("/practitioner/download")
def practitioner_download():
    filename = request.args.get("filename", "")
    content = None
    error = None
    if filename:
        # VULNERABLE: filter naif hanya menghapus '../' SATU KALI (non-recursive)
        sanitized = filename.replace("../", "")
        path = os.path.join(BASE_DIR, sanitized)
        try:
            with open(path, "r", errors="replace") as f:
                content = f.read(4000)
        except Exception as e:
            error = str(e)
    return render_template(
        "labs/pathtrav_practitioner.html", filename=filename, sanitized=sanitized if filename else "", content=content, error=error
    )


@bp.route("/expert/thumbnail")
def expert_thumbnail():
    filename = request.args.get("filename", "")
    content = None
    error = None
    blocked = False
    if filename:
        decoded = urllib.parse.unquote(filename)
        # VULNERABLE: validasi ekstensi dilakukan SEBELUM decode null-byte lama,
        # dan hanya mengecek literal '../' sebelum decoding penuh
        if "../" in filename:  # cek pada string ASLI (belum decode) -> bisa dilewati encoding
            blocked = True
        elif not decoded.split("%00")[0].endswith(".png") and "%00" not in filename:
            blocked = True
        else:
            real_path = decoded.split("%00")[0]
            path = os.path.join(BASE_DIR, real_path)
            try:
                with open(path, "r", errors="replace") as f:
                    content = f.read(4000)
            except Exception as e:
                error = str(e)
    return render_template(
        "labs/pathtrav_expert.html", filename=filename, content=content, error=error, blocked=blocked
    )
