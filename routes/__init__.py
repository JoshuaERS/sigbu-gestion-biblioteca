from .auth import bp as auth_bp
from .categorias import bp as categorias_bp
from .dashboard import bp as dashboard_bp
from .libros import bp as libros_bp
from .prestamos import bp as prestamos_bp
from .usuarios import bp as usuarios_bp


def register_blueprints(app):
    for blueprint in (dashboard_bp, auth_bp, categorias_bp, libros_bp, usuarios_bp, prestamos_bp):
        app.register_blueprint(blueprint)
