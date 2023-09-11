import json
from os.path import basename
from typing import Union

import flask


def open_json(filepath: str) -> dict:
    """ method opens json file """
    with open(filepath, 'r') as f:
        data: dict = json.load(f)
    return data


def save_json(filepath: str, data: dict):
    """ method saves json file """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def get_module_name(module: str) -> str:
    """ method returns module name without an extension"""
    return basename(module).split('.')[-1]


def response(
    data: dict, status: int = 200, mimetype: str = "application/json"
) -> flask.Response:
    return flask.Response(json.dumps(data), status=status, mimetype=mimetype)


def not_found_response(data: dict = None) -> flask.Response:
    data = data or {"error": "item not found"}

    return response(data, status=404)


def internal_error_response(data: dict = None) -> flask.Response:
    data = data or {"error": "internal server error"}

    return response(data, status=500)


def success_response(
    data: Union[dict, list] = None, message: str = None
) -> flask.Response:
    data = {"message": message} if message else (data or {"success": True})

    return response(data)
