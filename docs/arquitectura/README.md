# Arquitectura inicial

La aplicación sigue una organización por capas sencilla:

1. **Presentación:** plantillas Jinja, CSS y JavaScript.
2. **Aplicación:** rutas Flask organizadas en blueprints.
3. **Datos:** módulos de acceso a datos y base SQLite.

El patrón de fábrica `create_app` facilita las pruebas y la configuración futura.

