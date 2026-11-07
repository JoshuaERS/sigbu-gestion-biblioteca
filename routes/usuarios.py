import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.usuario import crear_usuario, listar_usuarios

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.get("/")
def index():
    return render_template("usuarios/index.html", usuarios=listar_usuarios(False))


@bp.route("/nuevo", methods=("GET", "POST"))
def nuevo():
    if request.method == "POST":
        try:
            crear_usuario(request.form["codigo"].strip(), request.form["nombre"].strip(), request.form["correo"].strip(), request.form["password"], request.form["rol"])
        except (KeyError, sqlite3.IntegrityError):
            flash("Revise los datos; el código y correo deben ser únicos.", "error")
        else:
            flash("Usuario registrado.", "success")
            return redirect(url_for("usuarios.index"))
    return render_template("usuarios/form.html")
