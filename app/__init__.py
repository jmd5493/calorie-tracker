from flask import Flask
from .routes import app_routes
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from .routes import app_routes
    app.register_blueprint(app_routes)

    return app


