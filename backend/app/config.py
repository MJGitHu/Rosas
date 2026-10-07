import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "rosas-secret-key-2026")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    PORT = int(os.getenv("PORT", 5000))
    
    # Parámetros de Oracle Database
    ORACLE_USER = os.getenv("ORACLE_USER", "ROSAS_ADMIN")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "Mariachi2026!")
    ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
    ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
    ORACLE_SERVICE_NAME = os.getenv("ORACLE_SERVICE_NAME", "XEPDB1")
    
    @property
    def ORACLE_DSN(self):
        return f"{self.ORACLE_HOST}:{self.ORACLE_PORT}/{self.ORACLE_SERVICE_NAME}"

    # Reglas de negocio
    ANTICIPO_PERCENTAGE = float(os.getenv("ANTICIPO_PERCENTAGE", 0.50))
    COMISION_TARJETA_PERCENTAGE = float(os.getenv("COMISION_TARJETA_PERCENTAGE", 0.035))
