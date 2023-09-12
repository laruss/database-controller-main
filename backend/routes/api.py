from flask import Blueprint

from backend.controllers.db_app.db_app_controllers import ItemFieldsController, ModelsController
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
    """
    Returns all models

    Returns:
        list of models as {"name": "route"}
    """
    return ModelsController().get_all()


@api_bp.route('/list/item/fields', methods=['GET'])
def get_list_item_fields():
    """
    Returns all fields of list item

    Returns:
        flask response with a list of objects fields as ["id", "name"]
    """
    return ItemFieldsController().get_all()
