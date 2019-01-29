import logging
import sys

LOGGER = logging.getLogger('bot_client')
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

import requests

from utils import get_config, BotClientError

config = get_config('config.json')
base_url = "{}:{}".format(config['network_host'], config['network_port'])

LOGGER = logging.getLogger('bot_client')


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


def get_user(id, token):
    resp = requests.get("{}/users/{}/".format(base_url, id),
                        headers={"Authorization": "Bearer {}".format(token)})

    if resp.status_code != 200:
        raise BotClientError("Failed to fetch user data")

    return resp.json()


def get_all_users():
    users = []
    page = 1
    while True:
        resp = requests.get(
            "{0}/users/?page={1}&page_size=10&likes__lt={2}&order_by=-posts_count".format(
                base_url, page, config['max_number_of_likes']))
        if resp.status_code == 404:
            break

        if resp.status_code != 200:
            raise BotClientError("Failed to fetch posts")

        json_data = resp.json()
        users += json_data['results']
        page += 1

    return users


def get_all_posts():
    posts = []
    page = 1
    while True:
        resp = requests.get("{}/posts/?page={}&page_size=100".format(base_url, page))
        if resp.status_code == 404:
            break

        if resp.status_code != 200:
            raise BotClientError("Failed to fetch posts")

        json_data = resp.json()
        posts += json_data['results']
        page += 1

    return posts


def perform_like(post, user, token):
    resp = requests.post("{}/posts/{}/like/".format(base_url, post['id']), json={},
                         headers={"Authorization": "Bearer {}".format(token)})

    if resp.status_code == 401 and resp.json()['code'] == 'token_not_valid':
        token, _ = obtain_token_pair(user['username'], config['default_password'])

        resp = requests.post("{}/posts/{}/like/".format(base_url, post['id']), json={},
                             headers={"Authorization": "Bearer {}".format(token)})

    if resp.status_code == 400:
        raise BotClientError("You can not like your own post or like a post multiple times.")

    if resp.status_code != 201:
        raise BotClientError("Unexpected error occured. Status code:{}".format(resp.status_code))
