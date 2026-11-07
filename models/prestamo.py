from datetime import date, timedelta

from flask import current_app

from . import get_db


def listar_prestamos(solo_activos=False):
    where = "WHERE p.estado = 'activo'" if solo_activos else ""
    return get_db().execute(
        f"""SELECT p.*, u.nombre AS usuario, u.codigo AS codigo_usuario,
                   e.codigo_inventario, l.titulo
            FROM prestamos p
            JOIN usuarios u ON u.id = p.usuario_id
            JOIN ejemplares e ON e.id = p.ejemplar_id
            JOIN libros l ON l.id = e.libro_id
            {where}
            ORDER BY p.estado, p.fecha_vencimiento, p.id DESC"""
    ).fetchall()


def registrar_prestamo(usuario_id, ejemplar_id, dias=7):
    database = get_db()
    hoy = date.today()
    with database:
        usuario = database.execute(
            "SELECT activo FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        ejemplar = database.execute(
            "SELECT estado FROM ejemplares WHERE id = ?", (ejemplar_id,)
        ).fetchone()
        if usuario is None or not usuario["activo"]:
            raise ValueError("El usuario no existe o está inactivo.")
        if ejemplar is None or ejemplar["estado"] != "disponible":
            raise ValueError("El ejemplar no está disponible.")
        reserva = None
        if current_app.config.get("RESERVAS_HABILITADAS"):
            reserva = database.execute(
                """SELECT * FROM reservas
                   WHERE ejemplar_id = ? AND estado IN ('activa', 'notificada')
                   ORDER BY turno, id LIMIT 1""",
                (ejemplar_id,),
            ).fetchone()
        if reserva is not None and reserva["usuario_id"] != usuario_id:
            raise ValueError("El ejemplar está reservado por otro usuario.")
        cursor = database.execute(
            """INSERT INTO prestamos
               (usuario_id, ejemplar_id, fecha_prestamo, fecha_vencimiento)
               VALUES (?, ?, ?, ?)""",
            (usuario_id, ejemplar_id, hoy.isoformat(), (hoy + timedelta(days=dias)).isoformat()),
        )
        database.execute("UPDATE ejemplares SET estado = 'prestado' WHERE id = ?", (ejemplar_id,))
        if reserva is not None:
            database.execute(
                "UPDATE reservas SET estado = 'atendida' WHERE id = ?", (reserva["id"],)
            )
    return cursor.lastrowid


def registrar_devolucion(prestamo_id):
    database = get_db()
    with database:
        prestamo = database.execute(
            "SELECT ejemplar_id, estado FROM prestamos WHERE id = ?", (prestamo_id,)
        ).fetchone()
        if prestamo is None:
            raise ValueError("El préstamo no existe.")
        if prestamo["estado"] != "activo":
            raise ValueError("El préstamo ya fue devuelto.")
        database.execute(
            "UPDATE prestamos SET estado = 'devuelto', fecha_devolucion = ? WHERE id = ?",
            (date.today().isoformat(), prestamo_id),
        )
        database.execute(
            "UPDATE ejemplares SET estado = 'disponible' WHERE id = ?",
            (prestamo["ejemplar_id"],),
        )
