import sqlite3
import secrets

from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db():
    with current_app.open_resource("database/schema.sql") as schema:
        get_db().executescript(schema.read().decode("utf-8"))


def crear_administrador_inicial():
    database = get_db()
    if database.execute("SELECT 1 FROM usuarios LIMIT 1").fetchone() is None:
        password = current_app.config["DEFAULT_ADMIN_PASSWORD"] or secrets.token_urlsafe(12)
        database.execute(
            """INSERT INTO usuarios (codigo, nombre, correo, password_hash, rol)
               VALUES (?, ?, ?, ?, 'administrador')""",
            ("ADMIN-001", "Administrador SIGBU", current_app.config["DEFAULT_ADMIN_EMAIL"], generate_password_hash(password)),
        )
        database.commit()
        if current_app.config["DEFAULT_ADMIN_PASSWORD"] is None:
            current_app.logger.warning(
                "Contraseña temporal del administrador %s: %s",
                current_app.config["DEFAULT_ADMIN_EMAIL"],
                password,
            )


def aplicar_migracion_reservas():
    if current_app.config.get("RESERVAS_HABILITADAS"):
        with current_app.open_resource("migrations/001_reservas_up.sql") as script:
            get_db().executescript(script.read().decode("utf-8"))


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
        aplicar_migracion_reservas()
        crear_administrador_inicial()

