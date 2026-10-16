import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    PORT = int(os.getenv("PORT", 5000))
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
    ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    FRONTEND_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGINS",
            "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    ]
    
    # Parámetros de Oracle Database
    ORACLE_USER = os.getenv("ORACLE_USER", "ROSAS_ADMIN")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
    ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
    ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
    ORACLE_SERVICE_NAME = os.getenv("ORACLE_SERVICE_NAME", "XEPDB1")
    
    @property
    def ORACLE_DSN(self):
        return f"{self.ORACLE_HOST}:{self.ORACLE_PORT}/{self.ORACLE_SERVICE_NAME}"

    # Reglas de negocio
    ANTICIPO_PERCENTAGE = float(os.getenv("ANTICIPO_PERCENTAGE", 0.50))
    COMISION_TARJETA = float(os.getenv("COMISION_TARJETA", 0.05))
    COMISION_TARJETA_PERCENTAGE = float(os.getenv("COMISION_TARJETA_PERCENTAGE", 0.05))
