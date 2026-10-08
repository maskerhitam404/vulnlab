import subprocess
import time
import re
from flask import Blueprint, request, render_template

bp = Blueprint("command_injection", __name__, url_prefix="/lab/command-injection")


@bp.route("/apprentice/ping")
def apprentice_ping():
    host = request.args.get("host", "")
    output = ""
    if host:
        # VULNERABLE: shell=True + string mentah dari user
        try:
            output = subprocess.run(
                f"ping -c 1 -W 1 {host}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout + subprocess.run(
                f"ping -c 1 -W 1 {host}", shell=True, capture_output=True, text=True, timeout=5
            ).stderr
        except Exception as e:
            output = str(e)
    return render_template("labs/cmdi_apprentice.html", host=host, output=output)


@bp.route("/practitioner/notify")
def practitioner_notify():
    email = request.args.get("email", "")
    sent = False
    if email:
        # VULNERABLE: dijalankan di background, tidak ada output yang pernah ditampilkan
        try:
            subprocess.run(f"echo notify {email} > /dev/null", shell=True, timeout=15)
            sent = True
        except Exception:
            sent = False
    return render_template("labs/cmdi_practitioner.html", email=email, sent=sent)


@bp.route("/expert/lookup")
def expert_lookup():
    domain = request.args.get("domain", "")
    output = ""
    blocked = False
    if domain:
        # Filter yang lupa memblokir pipe '|' dan $IFS
        if " " in domain or ";" in domain or "&&" in domain:
            blocked = True
        else:
            try:
                result = subprocess.run(
                    f"nslookup {domain}", shell=True, capture_output=True, text=True, timeout=5
                )
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)
    return render_template("labs/cmdi_expert.html", domain=domain, output=output, blocked=blocked)
