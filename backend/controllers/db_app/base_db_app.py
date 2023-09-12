from backend.controllers.base_controller import BC


"""
    This is a base service controller. 
    It will be reused by all the service controllers for database-controller
"""


class BaseDbAppController(BC):
    @BC._handle_errors
    def get_all(self):
        raise NotImplementedError

    def get_one_by_id(self, _id: str):
        raise NotImplementedError

    def create_one(self, data: dict):
        raise NotImplementedError

    def update_one_by_id(self, _id: str, data: dict):
        raise NotImplementedError

    def delete_one_by_id(self, _id: str):
        raise NotImplementedError

    def delete_all(self):
        raise NotImplementedError

    def get_schema(self):
        raise NotImplementedError
