# Registro de cambios

## 1.2.0 LB-02

Versión inicial estable con usuarios, catálogo, ejemplares, préstamos y devoluciones.

## 1.3.0 LB-03

- SCR: SCR-2026-001.
- Nueva tabla `reservas` con migración y reversión.
- Reserva, asignación de turno y cancelación.
- Límite de tres reservas pendientes por usuario.
- Integración con préstamos y devoluciones.
- Notificación idempotente de disponibilidad.
- Bandera `SIGBU_RESERVAS_HABILITADAS`.
- Pruebas automatizadas y documentación actualizada.
