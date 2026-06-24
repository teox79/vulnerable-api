"""Network diagnostics endpoint."""
import os

from flask import Blueprint, request

bp = Blueprint("diag", __name__)


@bp.get("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    return os.popen(f"ping -c 1 {host}").read()
