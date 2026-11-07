from werkzeug.security import generate_password_hash

from . import get_db


def listar_usuarios(activos=True):
    sql = "SELECT * FROM usuarios"
    if activos:
        sql += " WHERE activo = 1"
    return get_db().execute(sql + " ORDER BY nombre").fetchall()


def obtener_usuario(usuario_id):
    return get_db().execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()


def obtener_usuario_por_correo(correo):
    return get_db().execute("SELECT * FROM usuarios WHERE correo = ?", (correo,)).fetchone()


def crear_usuario(codigo, nombre, correo, password, rol="estudiante"):
    database = get_db()
    cursor = database.execute(
        """INSERT INTO usuarios (codigo, nombre, correo, password_hash, rol)
           VALUES (?, ?, ?, ?, ?)""",
        (codigo, nombre, correo.lower(), generate_password_hash(password), rol),
    )
    database.commit()
    return cursor.lastrowid

