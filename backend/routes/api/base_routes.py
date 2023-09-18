from typing import Type, List

from flask import request
from flask.views import MethodView

from pydantic_mongo import PydanticMongoModel as PmModel

import config
from backend.controllers.base_controller import BC
from backend.routes.utils import REGISTERED_ROUTES
from backend.helpers.constants import ROUTES_FILE
from backend.helpers.utils import open_json, save_json

filepath = config.routes_path / ROUTES_FILE


class BaseMV(MethodView):
    url_rule: str = '/{name}'
    name_rule: str = '{name}'

    url: str = None
    name: str = None
    controller: BC = None

    @classmethod
    def get_rule(cls) -> dict:
        return {
            'rule': cls.url,
            'view_func': cls.as_view(cls.name),
        }


class BR(BaseMV):
    def get(self):
        return self.controller.get_all()

    def post(self):
        return self.controller.create_one(request.json)

    def patch(self):
        raise NotImplementedError

    def delete(self):
        return self.controller.delete_all()


class BRItem(BaseMV):
    url_rule: str = '/{name}/<_id>'
    name_rule: str = '{name}-item'

    def get(self, _id: str):
        simplified = request.args.get('simplified', False)
        return self.controller.get_one_by_id(_id, simplified)

    def patch(self, _id: str):
        return self.controller.update_one_by_id(_id, request.json)

    def delete(self, _id: str):
        return self.controller.delete_one_by_id(_id)

    def post(self, _id: str):
        raise NotImplementedError


class BRSchema(BaseMV):
    url_rule: str = '/{name}/schema'
    name_rule: str = '{name}-schema'

    def get(self):
        return self.controller.get_schema()


class BaseRoute:
    name: str = None
    controller: BC = None
    routes: List[Type[BaseMV]] = [BR, BRItem, BRSchema]

    @classmethod
    def get_routes(cls) -> List[Type[BaseMV]]:
        routes = []
        for route in cls.routes:
            dyn_cls = type(route.__name__, (route,), {
                'name': route.name_rule.format(name=cls.name),
                'url': route.url_rule.format(name=cls.name),
                'controller': cls.controller
            })
            routes.append(dyn_cls)

        return routes


def _save_model_name_to_json(name: str, model: PmModel):
    """ method saves name and model name to json file if it doesn't exist """
    data = open_json(filepath)
    if name not in data.keys():
        data[name] = model.__name__
        save_json(filepath, data)


def get_routes_models_dict() -> dict:
    """ method returns dict with routes names and model names """
    return open_json(filepath)


def register_routes(route: Type[BaseRoute], save: bool = True) -> None:
    if save:
        _save_model_name_to_json(route.name, route.controller.model)
    REGISTERED_ROUTES.append({
        'name': route.name,
        'url_rules': [rt.get_rule() for rt in route.get_routes()]
    })
