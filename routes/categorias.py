from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.categoria import (
    crear_categoria,
    listar_categorias,
    obtener_categoria_por_nombre,
)


bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@bp.get("/")
def index():
    return render_template(
        "categorias/index.html",
        categorias=listar_categorias(),
    )


@bp.route("/nueva", methods=("GET", "POST"))
def nueva():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre:
            flash("El nombre de la categoría es obligatorio.", "error")
        elif len(nombre) > 80:
            flash("El nombre no puede superar 80 caracteres.", "error")
        elif obtener_categoria_por_nombre(nombre):
            flash("Ya existe una categoría con ese nombre.", "error")
        else:
            crear_categoria(nombre, descripcion)
            flash("Categoría registrada correctamente.", "success")
            return redirect(url_for("categorias.index"))

    return render_template("categorias/form.html")