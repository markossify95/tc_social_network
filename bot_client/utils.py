import json

class BotClientError(Exception):
    pass


def get_config(path):
    try:
        with open(path, 'r') as f:
            json_data = f.read()
            data = json.loads(json_data)
            return data
    except FileNotFoundError:
        return None
