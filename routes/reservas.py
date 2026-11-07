from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import get_db
from models.reserva import cancelar_reserva, crear_reserva, listar_reservas
from models.usuario import listar_usuarios

bp = Blueprint("reservas", __name__, url_prefix="/reservas")


def listar_ejemplares_prestados():
    return get_db().execute(
        """SELECT e.id, e.codigo_inventario, l.titulo, l.autor
           FROM ejemplares e JOIN libros l ON l.id = e.libro_id
           WHERE e.estado = 'prestado'
           ORDER BY l.titulo, e.codigo_inventario"""
    ).fetchall()


@bp.get("/")
def index():
    return render_template("reservas/index.html", reservas=listar_reservas())


@bp.route("/nueva", methods=("GET", "POST"))
def nueva():
    if request.method == "POST":
        try:
            crear_reserva(int(request.form["usuario_id"]), int(request.form["ejemplar_id"]))
        except (KeyError, ValueError) as error:
            flash(str(error) or "Datos inválidos.", "error")
        else:
            flash("Reserva registrada correctamente.", "success")
            return redirect(url_for("reservas.index"))
    return render_template(
        "reservas/form.html",
        usuarios=listar_usuarios(),
        ejemplares=listar_ejemplares_prestados(),
    )


@bp.post("/<int:reserva_id>/cancelar")
def cancelar(reserva_id):
    try:
        cancelar_reserva(reserva_id)
    except ValueError as error:
        flash(str(error), "error")
    else:
        flash("Reserva cancelada y turno liberado.", "success")
    return redirect(url_for("reservas.index"))
