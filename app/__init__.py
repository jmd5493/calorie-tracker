from flask import Flask
from .routes import app_routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['DATABASE'] = 'database/calorie.db'

    app.register_blueprint(app_routes)

    return app
