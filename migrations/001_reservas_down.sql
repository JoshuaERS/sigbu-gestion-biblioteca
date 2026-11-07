PRAGMA foreign_keys = ON;

DROP INDEX IF EXISTS ux_reserva_pendiente_usuario_ejemplar;
DROP INDEX IF EXISTS ix_reservas_usuario_estado;
DROP INDEX IF EXISTS ix_reservas_ejemplar_estado_turno;
DROP TABLE IF EXISTS reservas;
