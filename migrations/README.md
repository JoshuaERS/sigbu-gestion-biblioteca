# Migración del módulo de reservas

- `001_reservas_up.sql`: incorpora la tabla y sus índices sobre una base SIGBU v1.2.0.
- `001_reservas_down.sql`: revierte únicamente los objetos del módulo de reservas.

Ambos scripts deben probarse sobre una copia de la base antes del despliegue.
