import requests

from utils import get_config, BotClientError

config = get_config('config.json')
base_url = "{}:{}".format(config['network_host'], config['network_port'])


def obtain_token_pair(username, password):
    auth_data = {
        'username': username,
        'password': password
    }
    resp = requests.post(url="{}/auth/token/".format(base_url), json=auth_data)

    if resp.status_code != 200:
        raise BotClientError("Failed to obtain token pair")

    token_pair = resp.json()

    return token_pair['access'], token_pair['refresh']
