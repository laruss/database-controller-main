from controllers.UsersController import UsersController
from routes.BaseRoutes import *

name = __file__.split('/')[-1].split('.')[0]
controller = UsersController()


class UsersRoute(BR):
    _url = f'/{name}'
    _name = name
    _controller = controller


class UsersRouteItem(BRItem):
    _url = f'/{name}/<_id>'
    _name = f'{name}-item'
    _controller = controller


class UsersRouteScheme(BRScheme):
    _url = f'/{name}/scheme'
    _name = f'{name}-scheme'
    _controller = controller


users = get_route(name, UsersRoute, UsersRouteItem, UsersRouteScheme)
