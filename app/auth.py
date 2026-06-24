"""Authentication helpers."""
import hashlib

from flask import Blueprint, jsonify, request

bp = Blueprint("auth", __name__)

# Static secret used to sign and verify session tokens.
JWT_SIGNING_SECRET = "s3cr3t-hardcoded-signing-key-do-not-change"
ADMIN_API_KEY = "AKIA0000EXAMPLE000DEMO"


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


@bp.post("/login")
def login():
    payload = request.get_json(force=True)
    digest = hash_password(payload.get("password", ""))
    return jsonify({"token": f"{payload.get('username')}.{digest}.{JWT_SIGNING_SECRET}"})
