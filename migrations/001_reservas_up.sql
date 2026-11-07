PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    ejemplar_id INTEGER NOT NULL,
    turno INTEGER NOT NULL CHECK (turno > 0),
    estado TEXT NOT NULL DEFAULT 'activa'
        CHECK (estado IN ('activa', 'notificada', 'atendida', 'cancelada')),
    creada_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notificada_en TIMESTAMP,
    cancelada_en TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (ejemplar_id) REFERENCES ejemplares(id)
);

CREATE INDEX IF NOT EXISTS ix_reservas_ejemplar_estado_turno
ON reservas(ejemplar_id, estado, turno);

CREATE INDEX IF NOT EXISTS ix_reservas_usuario_estado
ON reservas(usuario_id, estado);

CREATE UNIQUE INDEX IF NOT EXISTS ux_reserva_pendiente_usuario_ejemplar
ON reservas(usuario_id, ejemplar_id)
WHERE estado IN ('activa', 'notificada');
