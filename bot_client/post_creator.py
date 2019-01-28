import logging
import random
import sys

import requests

from common import obtain_token_pair, base_url, config

LOGGER = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

def create_posts(user):
    access_token, refresh_token = obtain_token_pair(user['username'], config['default_password'])

    num_posts = random.randint(1, config['max_number_of_posts'])

    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
    }

    for i in range(num_posts):
        title = "{0} {1}".format(user['username'], str(i))
        content = "{0} says: {1}".format(user['username'], config['post_content'])

        payload = {
            "title": title,
            "content": content
        }

        resp = requests.post(url="{}/posts/".format(base_url), json=payload, headers=headers)

        if resp.status_code == 401 and resp.json()['code'] == 'token_not_valid':
            LOGGER.warning("{}. Obtaining new token pair...".format(resp.json()['messages'][0]['message']))
            access_token, refresh_token = obtain_token_pair(user['username'], config['default_password'])
            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            resp = requests.post(url="{}/posts/".format(base_url), json=payload, headers=headers)

        if resp.status_code != 201:
            LOGGER.error("Failed to create post. Response code: {}".format(resp.status_code))
