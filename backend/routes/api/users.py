from backend.controllers.user import UserController
from backend.helpers.utils import get_module_name
from backend.routes.api.base_routes import *


class UserRoure(BaseRoute):
    name = get_module_name(__name__)
    controller = UserController()


register_routes(UserRoure)
