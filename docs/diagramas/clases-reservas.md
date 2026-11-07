# Modelo de clases del módulo de reservas

```text
Usuario 1 -------- * Reserva * -------- 1 Ejemplar * -------- 1 Libro
                         |
                         +-- estado
                         +-- turno
                         +-- creada_en
                         +-- notificada_en
                         +-- cancelada_en

Usuario 1 -------- * Prestamo * -------- 1 Ejemplar
```

`Reserva` se relaciona con el usuario solicitante y el ejemplar prestado. La integración con `Prestamo` se realiza al devolver y al volver a prestar el ejemplar.
