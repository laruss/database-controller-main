from typing import Type

from flask import request
from flask.views import MethodView

from pydantic_mongo import PydanticMongoModel as PmModel

import config
from backend.controllers.base_controller import BC
from backend.helpers.constants import ROUTES_FILE
from backend.helpers.utils import open_json, save_json

filepath = config.routes_path / ROUTES_FILE


class BaseRoute(MethodView):
    _url: str = ''
    _name: str = ''
    _controller: BC = BC()

    @classmethod
    def get_rule(cls) -> dict:
        return {
            'rule': cls._url,
            'view_func': cls.as_view(cls._name),
        }


class BR(BaseRoute):
    def get(self):
        return self._controller.get_all()

    def post(self):
        data = request.json
        return self._controller.create_one(data)

    def patch(self):
        raise NotImplementedError

    def delete(self):
        return self._controller.delete_all()


class BRItem(BaseRoute):
    def get(self, _id: str):
        return self._controller.get_one_by_id(_id)

    def patch(self, _id: str):
        data = request.json
        return self._controller.update_one_by_id(_id, data)

    def delete(self, _id: str):
        return self._controller.delete_one_by_id(_id)

    def post(self, _id: str):
        raise NotImplementedError


class BRSchema(BaseRoute):
    def get(self):
        return self._controller.get_schema()


def _save_model_name_to_json(name: str, model: PmModel):
    """ method saves name and model name to json file if it doesn't exist """
    data = open_json(filepath)
    if name not in data.keys():
        data[name] = model.__name__
        save_json(filepath, data)


def get_routes_models_dict() -> dict:
    """ method returns dict with routes names and model names """
    return open_json(filepath)


def register_routes(name: str, *Routes: Type[BaseRoute], save=True):
    if not Routes:
        raise ValueError('Routes must be not empty')
    if save:
        _save_model_name_to_json(name, Routes[0]._controller.model)
    return {
        'name': name,
        'url_rules': [Route.get_rule() for Route in Routes]
    }
