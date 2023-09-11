import logging
import pathlib
from decouple import Config, RepositoryEnv


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

root_path = pathlib.Path(__file__).parent.resolve()
backend_path = root_path / "backend"
routes_path = backend_path / 'routes'

frontend_path = root_path / "frontend"
static_path = frontend_path / "static"
css_path = static_path / "css"
js_path = static_path / "js"

frontend_controller_path = root_path / "frontend-controller"
frontend_controller_static_path = frontend_controller_path / "static"

env_config = Config(RepositoryEnv(root_path / ".env"))


class DbConfig:
    DB_NAME = env_config.get("DB_NAME")
    HOST = env_config.get("DB_HOST")
    PORT = int(env_config.get("DB_PORT"))


class AppConfig:
    TESTING = True
    DEBUG = bool(env_config.get("DEBUG"))
    HOST = env_config.get("FLASK_APP_HOST")
    PORT = int(env_config.get("FLASK_APP_PORT"))
    MONGO_URI = f"mongodb://{DbConfig.HOST}:{DbConfig.PORT}/{DbConfig.DB_NAME}"
    MONGODB_SETTING = dict(
        db=DbConfig.DB_NAME,
        host=DbConfig.HOST,
        port=DbConfig.PORT
    )


class TestAppConfig:
    TESTING = True
    DEBUG = True
    HOST = "localhost"
    PORT = 5005
    MONGO_URI = "mongodb://localhost:27017/test_db"
