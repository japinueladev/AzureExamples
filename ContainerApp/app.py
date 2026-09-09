import os

from flask import Flask, jsonify, redirect, request
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
    return "Version 3.14"


@app.route('/profile/')
def profile():
    return {
        "name": "Juan Pérez",
        "profile_photo_url": "https://picsum.photos/200"
    }


@app.route('/profiles/')
def profiles():
    with engine.connect() as connection:
        rows = connection.execute(
            text("SELECT id, username, full_name, profile_photo_url FROM profiles")
        ).mappings().all()

    return jsonify([dict(row) for row in rows])


@app.route('/profile/<username>/photo')
def profile_photo(username):
    with engine.connect() as connection:
        row = connection.execute(
            text("SELECT profile_photo_url FROM profiles WHERE username = :username"),
            {"username": username}
        ).mappings().first()

    if row is None or not row["profile_photo_url"]:
        return {"status": "error", "error": "Profile not found"}, 404

    return redirect(row["profile_photo_url"])


@app.route('/profile/update-fullname/', methods=['POST'])
def profile_update_fullname():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    full_name = data.get("full_name")

    if not username or not full_name:
        return {"status": "error", "error": "username and full_name are required"}, 400

    with engine.begin() as connection:
        result = connection.execute(
            text("UPDATE profiles SET full_name = :full_name WHERE username = :username"),
            {"full_name": full_name, "username": username}
        )

        if result.rowcount == 0:
            return {"status": "error", "error": "Profile not found"}, 404

    return {"status": "ok", "username": username, "full_name": full_name}, 200


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


@app.route('/health-secret/')
def health_secret():
    database_url_secret = os.getenv("DATABASE_URL")

    if not database_url_secret:
        return {
            "status": "error",
            "database": "disconnected",
            "error": "DATABASE_URL environment variable is not set"
        }, 500

    try:
        secret_engine = create_engine(database_url_secret, pool_pre_ping=True)
        with secret_engine.connect() as connection:
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