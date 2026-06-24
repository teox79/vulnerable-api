"""Order lookup endpoints."""
from flask import Blueprint, jsonify, request

from .db import run_query

bp = Blueprint("orders", __name__)


@bp.get("/orders")
def search_orders():
    customer = request.args.get("customer", "")
    sql = f"SELECT id, total, status FROM orders WHERE customer = '{customer}'"
    rows = run_query(sql)
    return jsonify([dict(r) for r in rows])
