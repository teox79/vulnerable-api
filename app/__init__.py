"""Demo shop API — intentionally vulnerable, for security-tooling testing.

Wires the blueprints into a single Flask application.
"""
from flask import Flask

from . import auth, deserialize, exec, files, orders, users


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(users.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(files.bp)
    app.register_blueprint(exec.bp)
    app.register_blueprint(deserialize.bp)
    return app
