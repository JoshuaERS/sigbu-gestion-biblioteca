from flask import current_app

from . import get_db


ESTADOS_PENDIENTES = ("activa", "notificada")


def listar_reservas(usuario_id=None, solo_pendientes=False):
    condiciones, parametros = [], []
    if usuario_id is not None:
        condiciones.append("r.usuario_id = ?")
        parametros.append(usuario_id)
    if solo_pendientes:
        condiciones.append("r.estado IN ('activa', 'notificada')")
    where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    return get_db().execute(
        """SELECT r.*, u.nombre AS usuario, u.codigo AS codigo_usuario,
                  e.codigo_inventario, l.titulo
           FROM reservas r
           JOIN usuarios u ON u.id = r.usuario_id
           JOIN ejemplares e ON e.id = r.ejemplar_id
           JOIN libros l ON l.id = e.libro_id"""
        + where
        + " ORDER BY r.estado, r.ejemplar_id, r.turno, r.id",
        parametros,
    ).fetchall()


def obtener_reserva(reserva_id):
    return get_db().execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()


def obtener_primera_reserva_pendiente(ejemplar_id):
    return get_db().execute(
        """SELECT * FROM reservas
           WHERE ejemplar_id = ? AND estado IN ('activa', 'notificada')
           ORDER BY turno, id LIMIT 1""",
        (ejemplar_id,),
    ).fetchone()


def crear_reserva(usuario_id, ejemplar_id):
    database = get_db()
    with database:
        usuario = database.execute(
            "SELECT activo FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
        ejemplar = database.execute(
            "SELECT estado FROM ejemplares WHERE id = ?", (ejemplar_id,)
        ).fetchone()
        if usuario is None or not usuario["activo"]:
            raise ValueError("El usuario no existe o está inactivo.")
        if ejemplar is None:
            raise ValueError("El ejemplar no existe.")
        if ejemplar["estado"] != "prestado":
            raise ValueError("El ejemplar está disponible y puede prestarse directamente.")
        total_activas = database.execute(
            """SELECT COUNT(*) FROM reservas
               WHERE usuario_id = ? AND estado IN ('activa', 'notificada')""",
            (usuario_id,),
        ).fetchone()[0]
        if total_activas >= current_app.config["MAX_RESERVAS_ACTIVAS"]:
            raise ValueError(
                f"El usuario alcanzó el límite de {current_app.config['MAX_RESERVAS_ACTIVAS']} reservas activas."
            )
        duplicada = database.execute(
            """SELECT 1 FROM reservas
               WHERE usuario_id = ? AND ejemplar_id = ?
                 AND estado IN ('activa', 'notificada')""",
            (usuario_id, ejemplar_id),
        ).fetchone()
        if duplicada:
            raise ValueError("El usuario ya tiene una reserva pendiente para este ejemplar.")
        siguiente_turno = database.execute(
            """SELECT COALESCE(MAX(turno), 0) + 1 FROM reservas
               WHERE ejemplar_id = ? AND estado IN ('activa', 'notificada')""",
            (ejemplar_id,),
        ).fetchone()[0]
        cursor = database.execute(
            "INSERT INTO reservas (usuario_id, ejemplar_id, turno) VALUES (?, ?, ?)",
            (usuario_id, ejemplar_id, siguiente_turno),
        )
    return cursor.lastrowid


def cancelar_reserva(reserva_id, usuario_id=None):
    database = get_db()
    with database:
        reserva = database.execute(
            "SELECT * FROM reservas WHERE id = ?", (reserva_id,)
        ).fetchone()
        if reserva is None:
            raise ValueError("La reserva no existe.")
        if usuario_id is not None and reserva["usuario_id"] != usuario_id:
            raise ValueError("No puede cancelar la reserva de otro usuario.")
        if reserva["estado"] not in ESTADOS_PENDIENTES:
            raise ValueError("La reserva ya no está pendiente.")
        database.execute(
            """UPDATE reservas
               SET estado = 'cancelada', cancelada_en = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (reserva_id,),
        )
        database.execute(
            """UPDATE reservas SET turno = turno - 1
               WHERE ejemplar_id = ? AND turno > ?
                 AND estado IN ('activa', 'notificada')""",
            (reserva["ejemplar_id"], reserva["turno"]),
        )


def notificar_siguiente_reserva(ejemplar_id, database=None):
    database = database or get_db()
    reserva = database.execute(
        """SELECT r.id, r.usuario_id, u.nombre, u.correo
           FROM reservas r JOIN usuarios u ON u.id = r.usuario_id
           WHERE r.ejemplar_id = ? AND r.estado = 'activa'
           ORDER BY r.turno, r.id LIMIT 1""",
        (ejemplar_id,),
    ).fetchone()
    if reserva is None:
        return None
    actualizada = database.execute(
        """UPDATE reservas
           SET estado = 'notificada', notificada_en = CURRENT_TIMESTAMP
           WHERE id = ? AND estado = 'activa'""",
        (reserva["id"],),
    )
    return reserva if actualizada.rowcount == 1 else None
