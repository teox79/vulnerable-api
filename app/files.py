"""File download endpoint."""
import os

from flask import Blueprint, request, send_file

bp = Blueprint("files", __name__)

_BASE_DIR = "/srv/app/reports"


@bp.get("/download")
def download():
    name = request.args.get("path", "")
    full_path = os.path.join(_BASE_DIR, name)
    return send_file(full_path)
