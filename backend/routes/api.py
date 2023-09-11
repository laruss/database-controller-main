from flask import Blueprint

from backend.controllers.models_controller import ModelsController
from backend.helpers.utils import success_response
from backend.routes.users import users

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register all routes
for rules in [users]:
    [api_bp.add_url_rule(**rule) for rule in rules['url_rules']]


@api_bp.route('/', methods=['GET'])
def index():
    return success_response(message='API is working')


@api_bp.route('/models', methods=['GET'])
def get_models():
    return ModelsController().get_all()
