# Requisitos del módulo de reservas SIGBU 1.3

## RF-15 Reservar libro

Un usuario activo puede reservar un ejemplar que se encuentre prestado. El sistema asigna un turno consecutivo por ejemplar, impide duplicados y limita a tres las reservas pendientes de un usuario.

## RF-16 Notificar disponibilidad

Al registrar la devolución de un ejemplar, el sistema selecciona la primera reserva activa, cambia su estado a `notificada` y registra la fecha del aviso. La transición es atómica para evitar avisos duplicados.

## Reglas complementarias

- Un ejemplar disponible no se reserva porque puede prestarse directamente.
- Una reserva activa o notificada puede cancelarse y libera su turno.
- Un ejemplar con reserva pendiente no puede prestarse a una persona distinta del primer turno.
- Cuando el usuario beneficiario recibe el préstamo, su reserva cambia a `atendida`.
- Con la bandera desactivada, préstamos y devoluciones mantienen el comportamiento de SIGBU 1.2.0.
