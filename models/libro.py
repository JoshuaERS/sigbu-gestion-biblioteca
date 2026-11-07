from . import get_db


def listar_libros(busqueda=""):
    termino = f"%{busqueda.strip()}%"
    return get_db().execute(
        """
        SELECT l.*, c.nombre AS categoria,
               COUNT(e.id) AS total_ejemplares,
               SUM(CASE WHEN e.estado = 'disponible' THEN 1 ELSE 0 END) AS disponibles
        FROM libros l
        LEFT JOIN categorias c ON c.id = l.categoria_id
        LEFT JOIN ejemplares e ON e.libro_id = l.id
        WHERE l.activo = 1 AND (l.titulo LIKE ? OR l.autor LIKE ? OR l.isbn LIKE ?)
        GROUP BY l.id ORDER BY l.titulo
        """,
        (termino, termino, termino),
    ).fetchall()


def obtener_libro(libro_id):
    return get_db().execute("SELECT * FROM libros WHERE id = ?", (libro_id,)).fetchone()


def crear_libro(isbn, titulo, autor, editorial, anio_publicacion, categoria_id, descripcion=""):
    database = get_db()
    cursor = database.execute(
        """INSERT INTO libros
           (isbn, titulo, autor, editorial, anio_publicacion, categoria_id, descripcion)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (isbn, titulo, autor, editorial, anio_publicacion, categoria_id, descripcion),
    )
    database.commit()
    return cursor.lastrowid


def crear_ejemplar(libro_id, codigo_inventario, ubicacion=""):
    database = get_db()
    cursor = database.execute(
        "INSERT INTO ejemplares (libro_id, codigo_inventario, ubicacion) VALUES (?, ?, ?)",
        (libro_id, codigo_inventario, ubicacion),
    )
    database.commit()
    return cursor.lastrowid


def listar_ejemplares(libro_id=None, solo_disponibles=False):
    condiciones, parametros = [], []
    if libro_id:
        condiciones.append("e.libro_id = ?")
        parametros.append(libro_id)
    if solo_disponibles:
        condiciones.append("e.estado = 'disponible'")
    where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    return get_db().execute(
        """SELECT e.*, l.titulo, l.autor FROM ejemplares e
           JOIN libros l ON l.id = e.libro_id""" + where + " ORDER BY l.titulo, e.codigo_inventario",
        parametros,
    ).fetchall()
