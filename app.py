from pathlib import Path

from flask import Flask, redirect, request, session, url_for

from config import Config
from models import init_app as init_database
from routes import register_blueprints


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    init_database(app)
    register_blueprints(app)

    @app.before_request
    def exigir_inicio_de_sesion():
        rutas_publicas = {"auth.login", "static"}
        if request.endpoint not in rutas_publicas and "usuario_id" not in session:
            return redirect(url_for("auth.login", siguiente=request.full_path))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

