from flask import Blueprint, flash, redirect, render_template, request, url_for

from models.libro import listar_ejemplares
from models.prestamo import listar_prestamos, registrar_devolucion, registrar_prestamo
from models.usuario import listar_usuarios

bp = Blueprint("prestamos", __name__, url_prefix="/prestamos")


@bp.get("/")
def index():
    return render_template("prestamos/index.html", prestamos=listar_prestamos())


@bp.route("/nuevo", methods=("GET", "POST"))
def nuevo():
    if request.method == "POST":
        try:
            registrar_prestamo(int(request.form["usuario_id"]), int(request.form["ejemplar_id"]))
        except (KeyError, ValueError) as error:
            flash(str(error) or "Datos inválidos.", "error")
        else:
            flash("Préstamo registrado.", "success")
            return redirect(url_for("prestamos.index"))
    return render_template("prestamos/form.html", usuarios=listar_usuarios(), ejemplares=listar_ejemplares(solo_disponibles=True))


@bp.post("/<int:prestamo_id>/devolver")
def devolver(prestamo_id):
    try:
        registrar_devolucion(prestamo_id)
    except ValueError as error:
        flash(str(error), "error")
    else:
        flash("Devolución registrada.", "success")
    return redirect(url_for("prestamos.index"))
