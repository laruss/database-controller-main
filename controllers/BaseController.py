from functools import wraps

import flask
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine import ValidationError, Document, NotUniqueError, ReferenceField, ListField
from mongoengine.base import get_document

from helpers.constants import ROUTES_FILE
from helpers.path import Path
from helpers.utils import open_json


def get_routes_models_dict() -> dict:
    """ method returns dict with routes names and models names """
    filepath = f'{Path().routes_root}{ROUTES_FILE}'
    return open_json(filepath)


class BC:
    model = Document

    @staticmethod
    def response(data: dict | list, status: int = 200):
        if status < 100 or status > 599:
            raise ValueError("Status code must be between 100 and 599")
        return flask.jsonify(data), status

    def response404(self, caption: str):
        return self.response({'error': f'{caption} not found'}, status=404)

    def response204(self):
        return self.response({}, status=204)

    @staticmethod
    def strip_error(error: Exception):
        error = str(error)
        if 'class' in error:
            error = error.split("class")[-1].strip()
        return error

    @staticmethod
    def _handle_errors(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e.__class__.__name__}, {e}")
                if isinstance(e, InvalidId) or isinstance(e, ValidationError) or isinstance(e, NotUniqueError):
                    return BC.response(data={'error': BC.strip_error(e)}, status=400)

                # return BC.response(data={'error': str(e)}, status=500)
                raise e

        return wrapper

    def _get_object_by_id(self, _id: str, model: str | Document = None):
        model = get_document(model) if isinstance(model, str) else model
        model = model or self.model
        obj = model.objects(id=ObjectId(_id)).first()
        if obj:
            return obj

        raise ValidationError(f"{model.__class__.__name__} not found by id {_id}")

    @staticmethod
    def _check_has_references(instance: Document):
        routes_models_dict = get_routes_models_dict()
        for model_name in routes_models_dict.values():
            model = get_document(model_name)
            for field in model._fields.values():
                if isinstance(field, ReferenceField) and field.document_type == type(instance):
                    if model.objects(**{field.name: instance}).count() > 0:
                        return [model.objects(**{field.name: instance}).first().id, model_name]

        return None

    @staticmethod
    def obj_to_dict(obj):
        dict_ = obj.to_mongo()

        for field_name, field in dict_.items():
            if isinstance(field, ObjectId):
                dict_[field_name] = str(dict_[field_name])
        dict_['id'] = dict_.pop('_id')

        return dict_

    @staticmethod
    def _get_id_and_name(obj):
        return {'id': str(obj.id), 'name': obj.name}

    @_handle_errors
    def get_all(self):
        return self.response([self._get_id_and_name(obj) for obj in self.model.objects.all()])

    @_handle_errors
    def get_one_by_id(self, _id: str):
        obj = self._get_object_by_id(_id)

        return self.response(self.obj_to_dict(obj))

    def _handle_reference_field(self, field: ReferenceField, data: dict):
        if field.name in data:
            data[field.name] = self._get_object_by_id(data[field.name], field.document_type_obj)

    def _handle_body_data(self, data: dict):
        for field_name, field in self.model._fields.items():
            if isinstance(field, ReferenceField):
                self._handle_reference_field(field, data)
            elif isinstance(field, ListField):
                if isinstance(field.field, ReferenceField):
                    for i, item in enumerate(data[field_name]):
                        self._handle_reference_field(field.field, data[field_name][i])

        return data

    @_handle_errors
    def create_one(self, data: dict):
        data = self._handle_body_data(data)
        obj = self.model(**data)
        obj.save()

        return self.response(self.obj_to_dict(obj), 201)

    @_handle_errors
    def delete_one_by_id(self, _id: str):
        obj = self._get_object_by_id(_id)
        result = self._check_has_references(obj)
        if result:
            raise ValidationError(f"Can't delete {obj.__class__.__name__} with id {_id} because it has references "
                                  f"('{result[1]}' with id '{result[0]}')")

        obj.delete()

        return self.response204()

    @_handle_errors
    def update_one_by_id(self, _id: str, data: dict):
        data = self._handle_body_data(data)
        obj = self._get_object_by_id(_id)
        obj.update(**data)
        obj.save()
        obj = self._get_object_by_id(_id)

        return self.response(self.obj_to_dict(obj))

    def delete_all(self):
        [obj.delete() for obj in self.model.objects]

        return self.response204()

    def __get_scheme(self):
        result = {}
        for field_name, field in self.model._fields.items():
            field_type = type(field).__name__

            field_info = {
                "type": field_type,
                "required": field.required,
                "default": field.default if not callable(field.default) else None,
                "references": None
            }

            if isinstance(field, ReferenceField):
                field_info["references"] = field.document_type.__name__

            result[field_name] = field_info

        return result

    def get_scheme(self):
        return self.response(self.__get_scheme())
