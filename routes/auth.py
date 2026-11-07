from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from models.usuario import obtener_usuario_por_correo

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        usuario = obtener_usuario_por_correo(request.form.get("correo", "").strip().lower())
        if usuario and usuario["activo"] and check_password_hash(usuario["password_hash"], request.form.get("password", "")):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            flash("Sesión iniciada correctamente.", "success")
            destino = request.args.get("siguiente", "")
            return redirect(destino if destino.startswith("/") and not destino.startswith("//") else url_for("dashboard.index"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html")


@bp.post("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("dashboard.index"))
