from flask import Flask
from .config import Config
from .database import db
from .api.routes import api_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app) # Adiciona o suporte a CORS

    app.register_blueprint(api_bp, url_prefix='/api')

    return app

