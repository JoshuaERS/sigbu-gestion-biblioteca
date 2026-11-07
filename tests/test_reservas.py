import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app
from config import Config
from models import get_db
from models.libro import crear_ejemplar, crear_libro
from models.prestamo import registrar_devolucion, registrar_prestamo
from models.reserva import cancelar_reserva, crear_reserva, notificar_siguiente_reserva
from models.usuario import crear_usuario


class ReservasConfig(Config):
    TESTING = True
    SECRET_KEY = "test-reservas"
    DATABASE = Path(tempfile.gettempdir()) / "sigbu_reservas_test.db"
    DEFAULT_ADMIN_PASSWORD = "password-pruebas"
    RESERVAS_HABILITADAS = True
    MAX_RESERVAS_ACTIVAS = 3


class ReservasTestCase(unittest.TestCase):
    def setUp(self):
        ReservasConfig.DATABASE.unlink(missing_ok=True)
        self.app = create_app(ReservasConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            self.prestatario = crear_usuario("U-001", "Usuario prestatario", "prestatario@ucss.edu.pe", "clave")
            self.usuario = crear_usuario("U-002", "Usuario reserva", "reserva@ucss.edu.pe", "clave")
            self.otro_usuario = crear_usuario("U-003", "Segundo usuario", "segundo@ucss.edu.pe", "clave")
            self.ejemplares = []
            for numero in range(1, 5):
                libro = crear_libro(
                    f"97800000001{numero:02d}", f"Libro {numero}", "Autor", "Editorial", 2026, 1
                )
                ejemplar = crear_ejemplar(libro, f"EJ-{numero:03d}", "Estante A")
                registrar_prestamo(self.prestatario, ejemplar)
                self.ejemplares.append(ejemplar)

    def tearDown(self):
        ReservasConfig.DATABASE.unlink(missing_ok=True)

    def test_crea_reserva_valida_y_asigna_turnos(self):
        with self.app.app_context():
            primera = crear_reserva(self.usuario, self.ejemplares[0])
            segunda = crear_reserva(self.otro_usuario, self.ejemplares[0])
            filas = get_db().execute(
                "SELECT id, estado, turno FROM reservas ORDER BY turno"
            ).fetchall()
            self.assertEqual([fila["turno"] for fila in filas], [1, 2])
            self.assertEqual(filas[0]["id"], primera)
            self.assertEqual(filas[1]["id"], segunda)
            self.assertEqual(filas[0]["estado"], "activa")

    def test_rechaza_reserva_de_ejemplar_disponible(self):
        with self.app.app_context():
            registrar_devolucion(1)
            with self.assertRaisesRegex(ValueError, "puede prestarse directamente"):
                crear_reserva(self.usuario, self.ejemplares[0])

    def test_aplica_limite_de_tres_reservas_activas(self):
        with self.app.app_context():
            for ejemplar in self.ejemplares[:3]:
                crear_reserva(self.usuario, ejemplar)
            with self.assertRaisesRegex(ValueError, "límite de 3"):
                crear_reserva(self.usuario, self.ejemplares[3])

    def test_cancelacion_libera_y_reordena_turno(self):
        with self.app.app_context():
            primera = crear_reserva(self.usuario, self.ejemplares[0])
            segunda = crear_reserva(self.otro_usuario, self.ejemplares[0])
            cancelar_reserva(primera, self.usuario)
            estados = get_db().execute(
                "SELECT id, estado, turno FROM reservas ORDER BY id"
            ).fetchall()
            self.assertEqual(estados[0]["estado"], "cancelada")
            self.assertEqual(estados[1]["id"], segunda)
            self.assertEqual(estados[1]["turno"], 1)

    def test_devolucion_notifica_una_sola_vez(self):
        with self.app.app_context():
            reserva_id = crear_reserva(self.usuario, self.ejemplares[0])
            notificacion = registrar_devolucion(1)
            self.assertEqual(notificacion["usuario_id"], self.usuario)
            reserva = get_db().execute(
                "SELECT estado, notificada_en FROM reservas WHERE id = ?", (reserva_id,)
            ).fetchone()
            self.assertEqual(reserva["estado"], "notificada")
            self.assertIsNotNone(reserva["notificada_en"])
            self.assertIsNone(notificar_siguiente_reserva(self.ejemplares[0]))

    def test_bloquea_prestamo_reservado_por_otro_usuario(self):
        with self.app.app_context():
            crear_reserva(self.usuario, self.ejemplares[0])
            registrar_devolucion(1)
            with self.assertRaisesRegex(ValueError, "reservado por otro usuario"):
                registrar_prestamo(self.otro_usuario, self.ejemplares[0])
            registrar_prestamo(self.usuario, self.ejemplares[0])
            estado = get_db().execute("SELECT estado FROM reservas").fetchone()[0]
            self.assertEqual(estado, "atendida")

    def test_rutas_de_reservas_estan_activas_con_bandera(self):
        self.client.post(
            "/auth/login",
            data={"correo": ReservasConfig.DEFAULT_ADMIN_EMAIL, "password": ReservasConfig.DEFAULT_ADMIN_PASSWORD},
        )
        self.assertEqual(self.client.get("/reservas/").status_code, 200)
        self.assertEqual(self.client.get("/reservas/nueva").status_code, 200)


class MigracionReservasTestCase(unittest.TestCase):
    def test_migracion_y_reversion_preservan_tablas_base(self):
        ruta = Path(tempfile.gettempdir()) / "sigbu_migracion_reservas_test.db"
        ruta.unlink(missing_ok=True)
        database = sqlite3.connect(ruta)
        raiz = Path(__file__).resolve().parents[1]
        database.executescript((raiz / "database/schema.sql").read_text(encoding="utf-8"))
        database.executescript((raiz / "migrations/001_reservas_up.sql").read_text(encoding="utf-8"))
        self.assertIsNotNone(
            database.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservas'").fetchone()
        )
        database.executescript((raiz / "migrations/001_reservas_down.sql").read_text(encoding="utf-8"))
        self.assertIsNone(
            database.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservas'").fetchone()
        )
        self.assertIsNotNone(
            database.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prestamos'").fetchone()
        )
        database.close()
        ruta.unlink()


if __name__ == "__main__":
    unittest.main()
