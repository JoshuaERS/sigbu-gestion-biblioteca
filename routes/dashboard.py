from flask import Blueprint, render_template

from models import get_db

bp = Blueprint("dashboard", __name__)


@bp.get("/")
def index():
    database = get_db()
    resumen = {
        "libros": database.execute("SELECT COUNT(*) FROM libros WHERE activo = 1").fetchone()[0],
        "ejemplares_disponibles": database.execute("SELECT COUNT(*) FROM ejemplares WHERE estado = 'disponible'").fetchone()[0],
        "prestamos_activos": database.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'activo'").fetchone()[0],
        "usuarios": database.execute("SELECT COUNT(*) FROM usuarios WHERE activo = 1").fetchone()[0],
    }
    return render_template("dashboard.html", resumen=resumen)
