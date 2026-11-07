# Plan y registro de pruebas de reservas

## Alcance

Pruebas unitarias, integración, regresión, migración y reversión del cambio SCR-2026-001.

## Trazabilidad

| Caso de la práctica | Prueba automatizada | Resultado |
|---|---|---|
| UT-01 Crear reserva válida | `test_crea_reserva_valida_y_asigna_turnos` | Aprobado |
| UT-02 Rechazar ejemplar disponible | `test_rechaza_reserva_de_ejemplar_disponible` | Aprobado |
| UT-03 Límite de tres reservas | `test_aplica_limite_de_tres_reservas_activas` | Aprobado |
| UT-04 Cancelar reserva | `test_cancelacion_libera_y_reordena_turno` | Aprobado |
| UT-05 Asignar turnos | `test_crea_reserva_valida_y_asigna_turnos` | Aprobado |
| IT-02 Devolución y aviso único | `test_devolucion_notifica_una_sola_vez` | Aprobado |
| IT-03 Bloquear préstamo a tercero | `test_bloquea_prestamo_reservado_por_otro_usuario` | Aprobado |
| IT-04 Migración y reversión | `test_migracion_y_reversion_preservan_tablas_base` | Aprobado |
| RG-01 y RG-02 Circulación sin reservas | `test_prestamo_y_devolucion_actualizan_ejemplar` | Aprobado |
| RG-04 Bandera desactivada | suite `test_sigbu.py` | Aprobado |

## Resultado actual

Se ejecutaron 14 pruebas automatizadas y todas finalizaron correctamente. La aceptación visual y la cobertura porcentual se registrarán antes de fusionar a `main`.
