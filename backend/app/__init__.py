import atexit
from datetime import timedelta
from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from app.config import Config
from app.db import close_db_pool, init_db_pool


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGINS"]}},
        supports_credentials=True,
    )

    frontend_root = Path(__file__).resolve().parents[2] / "frontend"

    @app.route("/")
    def frontend_home():
        return send_from_directory(frontend_root / "public", "index.html")

    @app.route("/frontend/<path:filename>")
    def frontend_assets(filename):
        return send_from_directory(frontend_root, filename)
    
    # Inicializar pool de base de datos Oracle
    init_db_pool()
    atexit.register(close_db_pool)
    
    # Registrar Blueprints
    from app.routes.cotizaciones import cotizaciones_bp
    from app.routes.reservas import reservas_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(cotizaciones_bp, url_prefix="/api/cotizaciones")
    app.register_blueprint(reservas_bp, url_prefix="/api/reservas")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    
    @app.route("/api/health")
    def health_check():
        from app.db import _pool
        db_status = "connected" if _pool is not None else "disconnected"
        return {
            "status": "online",
            "app": "Rosas de Guadalupe Management System API",
            "version": "1.0.0",
            "database": db_status
        }
        
    return app
