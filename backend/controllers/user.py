from backend.controllers.base_controller import BC
from backend.models.user import User


class UserController(BC):
    model = User
