import random

from common import config, get_user, get_all_posts, obtain_token_pair, perform_like, LOGGER
from utils import BotClientError


class PostIterator:
    def __init__(self):
        self.user = {}
        self.posts = []
        self.access = None
        self.refresh = None

    def set_user(self, user):
        self.user = user

    def set_auth(self, access, refresh):
        self.access, self.refresh = access, refresh

    def set_posts(self, posts):
        self.posts = posts

    def _check_user_can_like(self):
        user = get_user(self.user['id'],
                        self.access)  # refresh count of likes every time. This enables opt. parallelism

        return user['like_count'] < config['max_number_of_likes']

    def _get_random_post(self):
        sanity_counter = 0  # used to check if posts without likes even exist (if we try too many times)

        while True:
            post = random.choice(self.posts)
            creator = get_user(post['user']['id'], self.access)
            if creator['has_unpopular_posts']:
                return post

            sanity_counter += 1
            if sanity_counter > config['max_number_of_posts']:
                self.posts = get_all_posts()  # refresh posts
                if not any([x['user']['has_unpopular_posts'] for x in self.posts]):
                    return None
                sanity_counter = 0

    def __iter__(self):
        if not self.user or not self.posts or not self.access:
            raise BotClientError("User was not provided, posts have not been fetched, or auth not set.")
        return self

    def __next__(self):
        if not self._check_user_can_like():  # user has reached max likes
            raise StopIteration
        target = self._get_random_post()
        if not target:  # no more posts without likes
            raise StopIteration

        return target


def like_em_all(users):
    iterator = PostIterator()

    for user in users:
        access, refresh = obtain_token_pair(user['username'], config['default_password'])
        iterator.set_auth(access, refresh)
        iterator.set_user(user)
        iterator.set_posts(get_all_posts())

        while True:
            try:
                post_to_like = next(iterator)
                perform_like(post=post_to_like, user=user, token=access)
            except StopIteration:
                break
            except BotClientError as e:
                LOGGER.warning("Failed to perform a like: {}".format(str(e)))
