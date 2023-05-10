import flask
from flask import Blueprint

from controllers.ModelsController import ModelsController
from routes.users import users

api_bp = Blueprint('api', __name__, url_prefix='/api')

for rules in [users]:
    [api_bp.add_url_rule(**rule) for rule in rules['url_rules']]


@api_bp.route('/', methods=['GET'])
def index():
    return flask.jsonify({'success': True, 'data': 'ping'})


@api_bp.route('/models', methods=['GET'])
def get_models():
    return ModelsController().get_all()
