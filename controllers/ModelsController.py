from controllers.BaseController import BC
from routes.BaseRoutes import get_routes_models_dict


class ModelsController(BC):
    def get_all(self):
        return self.response(get_routes_models_dict(), 200)
