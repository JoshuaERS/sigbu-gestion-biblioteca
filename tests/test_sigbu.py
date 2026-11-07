import tempfile
import unittest
from pathlib import Path

from app import create_app
from config import Config
from models import get_db
from models.libro import crear_ejemplar, crear_libro
from models.prestamo import registrar_devolucion, registrar_prestamo
from models.usuario import crear_usuario


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test"
    DATABASE = Path(tempfile.gettempdir()) / "sigbu_lb02_test.db"
    DEFAULT_ADMIN_PASSWORD = "password-exclusivo-de-pruebas"


class SigbuTestCase(unittest.TestCase):
    def setUp(self):
        TestConfig.DATABASE.unlink(missing_ok=True)
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        TestConfig.DATABASE.unlink(missing_ok=True)

    def iniciar_como_admin(self):
        return self.client.post(
            "/auth/login",
            data={"correo": TestConfig.DEFAULT_ADMIN_EMAIL, "password": TestConfig.DEFAULT_ADMIN_PASSWORD},
        )

    def crear_datos(self):
        with self.app.app_context():
            usuario_id = crear_usuario("2026001", "Ana Torres", "ana@ucss.edu.pe", "clave-segura")
            libro_id = crear_libro("9780000000001", "Ingeniería de software", "Ian Sommerville", "Pearson", 2016, 3)
            ejemplar_id = crear_ejemplar(libro_id, "ING-001", "Estante A1")
            return usuario_id, libro_id, ejemplar_id

    def test_paginas_principales_responden(self):
        self.iniciar_como_admin()
        for ruta in ("/", "/libros/", "/categorias/", "/usuarios/", "/prestamos/"):
            self.assertEqual(self.client.get(ruta).status_code, 200)

    def test_modulos_requieren_inicio_de_sesion(self):
        for ruta in ("/", "/libros/", "/categorias/", "/usuarios/", "/prestamos/"):
            respuesta = self.client.get(ruta)
            self.assertEqual(respuesta.status_code, 302)
            self.assertIn("/auth/login", respuesta.headers["Location"])
        self.assertEqual(self.client.get("/auth/login").status_code, 200)

    def test_registra_libro_y_ejemplar(self):
        self.iniciar_como_admin()
        respuesta = self.client.post("/libros/nuevo", data={"isbn": "9780000000002", "titulo": "Bases de datos", "autor": "Elmasri", "editorial": "Pearson", "anio_publicacion": "2017", "categoria_id": "3"})
        self.assertEqual(respuesta.status_code, 302)
        respuesta = self.client.post("/libros/1/ejemplares/nuevo", data={"codigo_inventario": "BD-001", "ubicacion": "Estante B2"})
        self.assertEqual(respuesta.status_code, 302)
        with self.app.app_context():
            self.assertEqual(get_db().execute("SELECT estado FROM ejemplares").fetchone()[0], "disponible")

    def test_prestamo_y_devolucion_actualizan_ejemplar(self):
        usuario_id, _, ejemplar_id = self.crear_datos()
        with self.app.app_context():
            prestamo_id = registrar_prestamo(usuario_id, ejemplar_id)
            self.assertEqual(get_db().execute("SELECT estado FROM ejemplares WHERE id = ?", (ejemplar_id,)).fetchone()[0], "prestado")
            registrar_devolucion(prestamo_id)
            self.assertEqual(get_db().execute("SELECT estado FROM ejemplares WHERE id = ?", (ejemplar_id,)).fetchone()[0], "disponible")

    def test_no_permite_prestar_ejemplar_no_disponible(self):
        usuario_id, _, ejemplar_id = self.crear_datos()
        with self.app.app_context():
            registrar_prestamo(usuario_id, ejemplar_id)
            with self.assertRaisesRegex(ValueError, "no está disponible"):
                registrar_prestamo(usuario_id, ejemplar_id)

    def test_inicio_de_sesion(self):
        self.crear_datos()
        respuesta = self.client.post("/auth/login", data={"correo": "ana@ucss.edu.pe", "password": "clave-segura"}, follow_redirects=True)
        self.assertIn("Sesión iniciada correctamente".encode("utf-8"), respuesta.data)


if __name__ == "__main__":
    unittest.main()
