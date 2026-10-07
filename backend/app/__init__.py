from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.db import init_db_pool, close_db_pool
import atexit

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Habilitar CORS para permitir llamadas desde el frontend
    CORS(app)
    
    # Inicializar pool de base de datos Oracle
    init_db_pool()
    atexit.register(close_db_pool)
    
    # Registrar Blueprints
    from app.routes.cotizaciones import cotizaciones_bp
    from app.routes.reservas import reservas_bp
    
    app.register_blueprint(cotizaciones_bp, url_prefix="/api/cotizaciones")
    app.register_blueprint(reservas_bp, url_prefix="/api/reservas")
    
    @app.route("/api/health")
    def health_check():
        return {
            "status": "online",
            "app": "Rosas de Guadalupe Management System API",
            "version": "1.0.0"
        }
        
    return app
