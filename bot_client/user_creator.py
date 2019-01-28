import json
import logging
import sys

import requests

from common import base_url, config
from utils import BotClientError

LOGGER = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


def fetch_emails(domain_name, user_count):
    api_key = config['hunter_api_key']
    endpoint = "https://api.hunter.io/v2/domain-search?domain={0}&api_key={1}&limit={2}".format(domain_name, api_key,
                                                                                                user_count)
    resp = requests.get(url=endpoint)

    if resp.status_code != 200:
        raise BotClientError("Failed to fetch emails.")

    try:
        email_objects = resp.json()['data']['emails']
        clean_emails = [e['value'] for e in email_objects]
        return clean_emails
    except KeyError:
        raise BotClientError("Unexpected response body.")


def create_users(emails):
    failed = []
    users = []

    for email in emails:
        username = email.split('@')[0]

        print(type(email))

        data = {
            'username': username,
            'password': config['default_password'],
            'email': email
        }

        dumped = json.dumps(data, ensure_ascii=False).encode('utf-8')

        resp = requests.post(url="{}/register/".format(base_url), data=dumped,
                             headers={'Content-Type': 'application/json;charset=UTF-8'})

        if resp.status_code == 400:
            failed.append(email)
            LOGGER.error("Failed to create account for email {0}. Response: {1}".format(email, str(resp.json())))

        if resp.status_code == 201:
            users.append(resp.json())
            LOGGER.info("Account successfully created.")

    return users, failed
