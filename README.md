# SIGBU

Sistema de Gestión de Biblioteca Universitaria con Flask y SQLite. La versión estable actual es `1.3.0`, línea base `LB-03`.

## Funcionalidades

- Categorías bibliográficas, libros y ejemplares físicos.
- Usuarios y roles, inicio y cierre de sesión.
- Préstamos, devoluciones y control de disponibilidad.
- Panel de indicadores y pruebas automatizadas.

## Ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app app run --debug
```

## Pruebas

```powershell
python -m unittest discover -v
```

La base `database.db` se crea automáticamente desde `database/schema.sql`.

## Módulo de reservas

La versión `1.3.0` incorpora reservas detrás de una bandera. Para habilitarla localmente:

```powershell
$env:SIGBU_RESERVAS_HABILITADAS = "true"
flask --app app run --debug
```

Al activarla, se aplica `migrations/001_reservas_up.sql`. Para el rollback se utiliza `migrations/001_reservas_down.sql`. El límite predeterminado es de tres reservas pendientes por usuario y puede configurarse mediante `SIGBU_MAX_RESERVAS`.

## Credenciales iniciales

Antes del primer inicio, defina una contraseña local para el administrador:

```powershell
$env:SIGBU_ADMIN_EMAIL = "admin@sigbu.local"
$env:SIGBU_ADMIN_PASSWORD = "una-clave-segura"
flask --app app run --debug
```

Si no se define una contraseña, el sistema genera una temporal y la muestra únicamente en la consola durante la creación de la base. Las credenciales y la base local no se versionan.
