import functools
from typing import Optional, List

import flask
from pydantic_mongo import PydanticMongoModel as PmModel
from pydantic_mongo.extensions import ValidationError

import config
from backend.helpers.constants import ROUTES_FILE
from backend.helpers.utils import open_json, response, not_found_response


def get_routes_models_dict() -> dict:
    """ method returns dict with routes names and model names """
    filepath = config.routes_path / ROUTES_FILE
    return open_json(filepath)


class BC:
    model = PmModel

    def _get_by_id(self, _id: str) -> PmModel:
        instance = self.model.get_by_id(_id)
        if not instance:
            raise KeyError(f"Can't find {self.model.__name__} with id {_id}")

        return instance

    @staticmethod
    def _handle_errors(func):
        @functools.wraps(func)
        def wrapper_error_handler(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if isinstance(e, IndexError) or isinstance(e, KeyError):
                    return BC.response404(f"{e}")
                else:
                    raise e

        return wrapper_error_handler

    @staticmethod
    def response(data: dict | list, status: int = 200) -> flask.Response:
        if status < 100 or status > 599:
            raise ValueError("Status code must be between 100 and 599")
        return response(data, status)

    @staticmethod
    def response404(caption: str) -> flask.Response:
        return not_found_response({"error": f"{caption} not found"})

    def response204(self):
        return self.response({"success": True}, status=204)

    @staticmethod
    def _check_has_references(instance: PmModel) -> Optional[List[Optional[PmModel]]]:
        return instance.get_ref_objects()

    @_handle_errors
    def get_all(self, **filters):
        return self.response(list(self.model.objects(filter=filters)))

    @_handle_errors
    def get_one_by_id(self, _id: str):
        return self.response(self._get_by_id(_id).model_dump())

    @_handle_errors
    def create_one(self, data: dict):
        instance = self.model(**data).save()

        return self.response(instance.model_dump(), 201)

    @_handle_errors
    def delete_one_by_id(self, _id: str):
        instance = self._get_by_id(_id)
        result = instance.get_ref_objects()
        if result:
            raise ValidationError(
                f"Can't delete {self.model.__class__.__name__} with id {_id} because it has references "
                f"('{result[1]}' with id '{result[0]}')"
            )

        instance.delete()

        return self.response204()

    @_handle_errors
    def update_one_by_id(self, _id: str, data: dict):
        instance = self._get_by_id(_id)

        full_data = {**instance.model_dump(), **data}
        self.model(**full_data).save()

        return self.response204()

    def delete_all(self):
        [obj.delete() for obj in self.model.objects()]

        return self.response204()

    def get_schema(self):
        return self.response(self.model.model_json_schema(True))
