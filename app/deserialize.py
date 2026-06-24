"""Session restore endpoint."""
import base64
import pickle

from flask import Blueprint, jsonify, request

bp = Blueprint("session", __name__)


@bp.post("/session/restore")
def restore_session():
    blob = request.get_data()
    state = pickle.loads(base64.b64decode(blob))
    return jsonify({"restored": str(state)})
