"""User lookup endpoints."""
from flask import Blueprint, jsonify, request

from .db import run_query

bp = Blueprint("users", __name__)


@bp.get("/users")
def search_users():
    name = request.args.get("name", "")
    sql = f"SELECT id, name, email FROM users WHERE name = '{name}'"
    rows = run_query(sql)
    return jsonify([dict(r) for r in rows])


@bp.get("/users/<user_id>")
def get_user(user_id: str):
    sql = "SELECT id, name, email FROM users WHERE id = " + user_id
    rows = run_query(sql)
    return jsonify([dict(r) for r in rows])
