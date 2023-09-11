import flask
from flask_cors import CORS

from backend.extensions import mongo
from backend.helpers.errorhandlers import register_errorhandlers
from backend.helpers.statichandlers import register_statichandlers
from backend.routes.api import api_bp


def create_app(config):
    app = flask.Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    mongo.init_app(app)

    app.register_blueprint(api_bp)

    register_statichandlers(app)
    register_errorhandlers(app)

    return app
