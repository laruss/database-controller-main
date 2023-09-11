from backend.controllers.user import UsersController
from backend.helpers.utils import get_module_name
from backend.routes.base_routes import *

name = get_module_name(__name__)
controller = UsersController()


class UsersRoute(BR):
    _url = f'/{name}'
    _name = name
    _controller = controller


class UsersRouteItem(BRItem):
    _url = f'/{name}/<_id>'
    _name = f'{name}-item'
    _controller = controller


class UsersRouteSchema(BRSchema):
    _url = f'/{name}/schema'
    _name = f'{name}-schema'
    _controller = controller


users = register_routes(name, UsersRoute, UsersRouteItem, UsersRouteSchema)
