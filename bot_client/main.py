import logging
import sys

from common import config
from post_creator import create_posts
from user_creator import fetch_emails, create_users

LOGGER = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

def run():
    LOGGER.info("fetching emails...")
    emails = fetch_emails(domain_name='trello.com', user_count=config['number_of_users'])
    LOGGER.info("emails fetched: {}".format(str(emails)))

    LOGGER.info("creating users...")
    users, failed = create_users(emails)
    LOGGER.info("Users successfully created: {}".format(str(users)))
    LOGGER.info("Failed to create: {}".format(str(failed)))

    for u in users:
        LOGGER.info("Spamming the network in name of a user {}".format(str(u)))
        create_posts(u)


if __name__ == '__main__':
    run()
