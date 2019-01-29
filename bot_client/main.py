from common import config, get_all_users, LOGGER
from liker import like_em_all
from post_creator import create_posts
from user_creator import fetch_emails, create_users


def run():
    LOGGER.info("fetching emails...")
    emails = fetch_emails(domain_name=config['source_domain_name'], user_count=config['number_of_users'])
    LOGGER.info("emails fetched: {}".format(str(emails)))

    LOGGER.info("creating users...")
    users, failed = create_users(emails)
    LOGGER.info("Users successfully created: {}".format(str(users)))
    LOGGER.info("Failed to create: {}".format(str(failed)))

    for u in users:
        LOGGER.info("Spamming the network in name of a user {}".format(str(u)))
        create_posts(u)

    users = get_all_users()  # refresh user objects to order them properly using backend
    users = [u for u in users if u['username'] != 'admin']  # exclude the admin because of failed auth
    like_em_all(users)


if __name__ == '__main__':
    run()
