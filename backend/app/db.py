import oracledb
from app.config import Config

config = Config()

_pool = None

def init_db_pool():
    """
    Inicializa el pool de conexiones a Oracle Database en modo Thin.
    """
    global _pool
    if not config.ORACLE_PASSWORD:
        print("[DB ERROR] ORACLE_PASSWORD no está configurada; define las credenciales locales en backend/.env.")
        _pool = None
        return

    try:
        # Modo Thin activado por defecto (no requiere Oracle Instant Client local)
        _pool = oracledb.create_pool(
            user=config.ORACLE_USER,
            password=config.ORACLE_PASSWORD,
            dsn=config.ORACLE_DSN,
            min=2,
            max=10,
            increment=1
        )
        print(f"[DB] Conexión establecida con Oracle Database en {config.ORACLE_DSN}")
    except oracledb.Error as err:
        print(f"[DB WARNING] No se pudo inicializar el pool de Oracle DB: {err}")
        print("[DB WARNING] La aplicación operará en modo offline/mock para desarrollo inicial.")
        _pool = None

def get_db_connection():
    """
    Retorna una conexión activa del pool de Oracle.
    """
    global _pool
    if _pool:
        return _pool.acquire()
    return None

def close_db_pool():
    """
    Cierra de forma segura el pool de conexiones al terminar la app.
    """
    global _pool
    if _pool:
        _pool.close()
        print("[DB] Pool de Oracle cerrado correctamente.")
