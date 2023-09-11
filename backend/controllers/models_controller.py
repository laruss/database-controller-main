from backend.controllers.base_controller import BC
from backend.routes.base_routes import get_routes_models_dict


class ModelsController(BC):
    def get_all(self):
        return self.response(get_routes_models_dict(), 200)
