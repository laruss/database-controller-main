from backend.controllers.base_controller import BC
from backend.models.user import User


class UsersController(BC):
    model = User
