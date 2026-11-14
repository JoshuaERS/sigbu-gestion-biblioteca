# Cierre de SCR-2026-001

## Objetivo

Incorporar el módulo de reservas de ejemplares a SIGBU y establecer la versión 1.3.0 como línea base LB-03.

## Alcance implementado

- Migración y reversión de la tabla de reservas.
- Registro, asignación de turnos y cancelación de reservas.
- Límite configurable de reservas activas por usuario.
- Integración con préstamos, devoluciones y usuarios.
- Notificación idempotente de disponibilidad.
- Bandera de activación `SIGBU_RESERVAS_HABILITADAS`.
- Pruebas automatizadas y documentación funcional.

## Verificación

La ejecución de `python -m unittest discover -v` finalizó correctamente con 14 pruebas aprobadas.

## Trazabilidad

- Rama funcional: `feature/SCR-2026-001`.
- Versión anterior: `v1.2.0` / `LB-02`.
- Versión liberada: `v1.3.0` / `LB-03`.
- Integración: commit `9a60a4b`.
- Liberación: commit `09abfbc`.

## Nota de proceso

La integración funcional fue realizada directamente en `main`. Este documento y su Pull Request registran la revisión y el cierre posterior del cambio sin modificar el historial de la versión publicada.
