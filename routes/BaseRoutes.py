from typing import Type

from flask import request
from flask.views import MethodView
from mongoengine import Document

from controllers.BaseController import BC
from helpers.constants import ROUTES_FILE
from helpers.path import Path
from helpers.utils import open_json, save_json


class BaseRoute(MethodView):
    _url = ''
    _name = ''
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


class BRScheme(BaseRoute):
    def get(self):
        return self._controller.get_scheme()


def _save_name_model_name_to_json(name: str, model: Document):
    """ method saves name and model name to json file if doesn't exist """
    filepath = f'{Path().routes_root}{ROUTES_FILE}'
    data = open_json(filepath)
    if name not in data.keys():
        data[name] = model.__name__
        save_json(filepath, data)


def get_routes_models_dict() -> dict:
    """ method returns dict with routes names and models names """
    filepath = f'{Path().routes_root}{ROUTES_FILE}'
    return open_json(filepath)


def get_route(name: str, *Routes: Type[BaseRoute], save=True):
    if not Routes:
        raise ValueError('Routes must be not empty')
    if save:
        _save_name_model_name_to_json(name, Routes[0]._controller.model)
    return {
        'name': name,
        'url_rules': [Route.get_rule() for Route in Routes]
    }
