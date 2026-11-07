from . import get_db


def listar_categorias():
    return get_db().execute(
        """
        SELECT id, nombre, descripcion, creado_en
        FROM categorias
        ORDER BY nombre
        """
    ).fetchall()


def obtener_categoria_por_nombre(nombre):
    return get_db().execute(
        """
        SELECT id, nombre, descripcion
        FROM categorias
        WHERE LOWER(nombre) = LOWER(?)
        """,
        (nombre,),
    ).fetchone()


def crear_categoria(nombre, descripcion=""):
    database = get_db()
    cursor = database.execute(
        """
        INSERT INTO categorias (nombre, descripcion)
        VALUES (?, ?)
        """,
        (nombre, descripcion),
    )
    database.commit()
    return cursor.lastrowid