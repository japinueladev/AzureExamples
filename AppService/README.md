# AppService

Ejemplo básico de una aplicación Flask pensada para desplegarse en Azure App Service.

## Requisitos

- Python 3.x
- Dependencias listadas en [requirements.txt](requirements.txt): `flask`, `gunicorn`, `pymysql`, `sqlalchemy`

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución local

```bash
python app.py
```

La aplicación arranca en `http://0.0.0.0:8080`.

## Endpoints

| Método | Ruta        | Descripción                                  |
|--------|-------------|-----------------------------------------------|
| GET    | `/`         | Devuelve un saludo de prueba ("Hola mundo")   |
| GET    | `/profile/` | Devuelve un JSON de ejemplo con datos de perfil |

## Despliegue en Azure App Service

Al desplegar en Azure App Service, este servicio se sirve normalmente con `gunicorn`, por ejemplo:

```bash
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```
