from backend.controllers.db_app.base_db_app import BaseDbAppController
from backend.routes.api.base_routes import get_routes_models_dict


"""
    This is a controller for the models route.
    It is used to get all the models in the app.
"""


class ModelsController(BaseDbAppController):
    @BaseDbAppController._handle_errors
    def get_all(self):
        return self.response(get_routes_models_dict(), 200)


class ItemFieldsController(BaseDbAppController):
    @BaseDbAppController._handle_errors
    def get_all(self):
        return self.response([field for field in self.model.model_fields.keys()])
