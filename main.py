import flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from mongoengine import ValidationError, DoesNotExist, FieldDoesNotExist

from config import Config
from routes.api import api_bp


db = MongoEngine()
app = flask.Flask("example_app")
app.config["MONGODB_SETTINGS"] = [Config]
db.init_app(app)
CORS(app)

app.register_blueprint(api_bp)


@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return flask.jsonify({'success': False, 'errors': str(err)}), 400


@app.errorhandler(DoesNotExist)
def handle_does_not_exist(err):
    return flask.jsonify({'success': False, 'errors': str(err)}), 404


@app.errorhandler(FieldDoesNotExist)
def handle_field_does_not_exist(err):
    return flask.jsonify({'success': False, 'errors': str(err)}), 404


@app.errorhandler(405)
def handle_405(err):
    return flask.jsonify({'success': False, 'errors': '405 Method Not Allowed'}), 405


@app.errorhandler(404)
def handle_404(err):
    return flask.jsonify({'success': False, 'errors': f'{err}'}), 404


if __name__ == '__main__':
    app.run(debug=True)
