from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    config = Config()
    print(f"Servidor backend ejecutándose en http://localhost:{config.PORT}")
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG)
