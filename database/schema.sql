PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'estudiante'
        CHECK (rol IN ('estudiante', 'bibliotecario', 'administrador')),
    activo INTEGER NOT NULL DEFAULT 1,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    editorial TEXT,
    anio_publicacion INTEGER,
    categoria_id INTEGER,
    descripcion TEXT,
    activo INTEGER NOT NULL DEFAULT 1,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS ejemplares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id INTEGER NOT NULL,
    codigo_inventario TEXT NOT NULL UNIQUE,
    ubicacion TEXT,
    estado TEXT NOT NULL DEFAULT 'disponible'
        CHECK (estado IN ('disponible', 'prestado', 'inactivo')),
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (libro_id) REFERENCES libros(id)
);

CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    ejemplar_id INTEGER NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    fecha_devolucion DATE,
    estado TEXT NOT NULL DEFAULT 'activo'
        CHECK (estado IN ('activo', 'devuelto')),
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (ejemplar_id) REFERENCES ejemplares(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_prestamo_activo_ejemplar
ON prestamos(ejemplar_id) WHERE estado = 'activo';

INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES
    ('Ciencias', 'Ciencias naturales, exactas y aplicadas'),
    ('Humanidades', 'Historia, filosofía, literatura y arte'),
    ('Ingeniería', 'Tecnología e ingeniería');

