import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def variable_booleana(nombre, predeterminado=False):
    valor = os.getenv(nombre)
    if valor is None:
        return predeterminado
    return valor.strip().lower() in {"1", "true", "si", "sí", "on"}


class Config:
    SECRET_KEY = "desarrollo-sigbu-cambiar-en-produccion"
    DATABASE = BASE_DIR / "database.db"
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    VERSION = "1.2.0"
    LINEA_BASE = "LB-02"
    DEFAULT_ADMIN_EMAIL = os.getenv("SIGBU_ADMIN_EMAIL", "admin@sigbu.local")
    DEFAULT_ADMIN_PASSWORD = os.getenv("SIGBU_ADMIN_PASSWORD")
    MAX_RESERVAS_ACTIVAS = int(os.getenv("SIGBU_MAX_RESERVAS", "3"))
    RESERVAS_HABILITADAS = variable_booleana("SIGBU_RESERVAS_HABILITADAS", False)

