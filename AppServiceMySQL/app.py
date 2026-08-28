from flask import Flask
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Conexión directa SOLO para primera prueba
DB_HOST = "practica1-mysql.mysql.database.azure.com"
DB_PORT = 3306
DB_USER = "practica1"
DB_PASSWORD = "395wMljoFdKWgcClKZqG"
DB_NAME = "perfilesdb"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


@app.route('/')
def index():
    return "Hola mundo"


@app.route('/profile/')
def profile():
    return {
        "name": "Juan Pérez",
        "profile_photo_url": "https://picsum.photos/200"
    }


@app.route('/health/')
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }, 200

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }, 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)