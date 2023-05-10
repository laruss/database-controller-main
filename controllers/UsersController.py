from controllers.BaseController import BC
from models.User import User


class UsersController(BC):
    model = User
