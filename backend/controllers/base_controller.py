import functools
from typing import Optional, List

import flask
from pydantic_mongo.extensions import ValidationError

import config
from backend.helpers.constants import ROUTES_FILE
from backend.helpers.utils import open_json, response, not_found_response
from backend.models.base import BaseAppModel


def get_routes_models_dict() -> dict:
    """ method returns dict with routes names and model names """
    filepath = config.routes_path / ROUTES_FILE
    return open_json(filepath)


class BC:
    model = BaseAppModel

    def _get_by_id(self, _id: str) -> BaseAppModel:
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
            except ValidationError as e:
                return BC.response({"error": f"{e}"}, status=400)
            except KeyError as e:
                return BC.response404(f"{e}")
            except IndexError as e:
                return BC.response404(f"{e}")
            except Exception as e:
                return BC.response({"error": f"{e}"}, status=500)

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
    def _check_has_references(instance: BaseAppModel) -> Optional[List[Optional[BaseAppModel]]]:
        return instance.get_ref_objects()

    @_handle_errors
    def get_all(self, **filters):
        fields_to_get = BaseAppModel.model_fields.keys()
        result = []

        for instance in self.model.objects(**filters):
            dump = instance.model_dump()
            result.append({field: dump[field] for field in fields_to_get})

        return self.response(result)

    @_handle_errors
    def get_one_by_id(self, _id: str, simplified: bool = False):
        result = self._get_by_id(_id)
        result = result.model_dump(True)
        result = self._get_simplified(result) if simplified else result

        return self.response(result)

    @staticmethod
    def _get_simplified(dump: dict) -> dict:
        fields_to_get = BaseAppModel.model_fields.keys()
        return {field: dump[field] for field in fields_to_get}

    @_handle_errors
    def create_one(self, data: dict):
        instance = self.model.get_with_parse_db_refs(data).save()

        return self.response(instance.model_dump(), 201)

    @_handle_errors
    def delete_one_by_id(self, _id: str):
        instance = self._get_by_id(_id)
        result = instance.get_ref_objects()
        if result:
            for inst in result:
                if inst.id:
                    raise ValidationError(
                        f"Can't delete {self.model.__class__.__name__} with id {_id} because it has references "
                        f"('{instance.__class__.__name__}' with id '{instance.id}')"
                    )

        instance.delete()
        return self.response204()

    @_handle_errors
    def update_one_by_id(self, _id: str, data: dict):
        data.pop('id', None)
        instance = self.model.get_with_parse_db_refs(data)
        instance.id = _id
        instance.save()

        return self.response204()

    def delete_all(self):
        [obj.delete() for obj in self.model.objects()]

        return self.response204()

    def get_schema(self):
        schema = self.model.model_json_schema(True)
        schema['title'] = self.model.__name__
        required: list = schema.get('required', [])
        schema['required'] = [field for field in required if field != 'id']
        return self.response(schema)
