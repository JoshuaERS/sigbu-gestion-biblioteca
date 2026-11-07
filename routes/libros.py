import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.categoria import listar_categorias
from models.libro import crear_ejemplar, crear_libro, listar_ejemplares, listar_libros, obtener_libro

bp = Blueprint("libros", __name__, url_prefix="/libros")


@bp.get("/")
def index():
    return render_template("libros/index.html", libros=listar_libros(request.args.get("q", "")))


@bp.route("/nuevo", methods=("GET", "POST"))
def nuevo():
    if request.method == "POST":
        try:
            crear_libro(request.form["isbn"].strip(), request.form["titulo"].strip(), request.form["autor"].strip(), request.form.get("editorial", "").strip(), int(request.form["anio_publicacion"]) if request.form.get("anio_publicacion") else None, int(request.form["categoria_id"]) if request.form.get("categoria_id") else None, request.form.get("descripcion", "").strip())
        except (KeyError, ValueError, sqlite3.IntegrityError):
            flash("Revise los datos; el ISBN debe ser único.", "error")
        else:
            flash("Libro registrado.", "success")
            return redirect(url_for("libros.index"))
    return render_template("libros/form.html", categorias=listar_categorias())


@bp.route("/<int:libro_id>/ejemplares/nuevo", methods=("GET", "POST"))
def nuevo_ejemplar(libro_id):
    libro = obtener_libro(libro_id)
    if libro is None:
        return "Libro no encontrado", 404
    if request.method == "POST":
        try:
            crear_ejemplar(libro_id, request.form["codigo_inventario"].strip(), request.form.get("ubicacion", "").strip())
        except (KeyError, sqlite3.IntegrityError):
            flash("El código de inventario es obligatorio y debe ser único.", "error")
        else:
            flash("Ejemplar registrado.", "success")
            return redirect(url_for("libros.index"))
    return render_template("libros/ejemplar_form.html", libro=libro, ejemplares=listar_ejemplares(libro_id))
