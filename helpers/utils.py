import json


def open_json(filepath: str) -> dict:
    """ method opens json file """
    f = open(filepath, 'r')
    data: dict = json.load(f)
    f.close()
    return data


def save_json(filepath: str, data: dict):
    """ method saves json file """
    f = open(filepath, 'w')
    json.dump(data, f, indent=4)
    f.close()
