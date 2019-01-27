from __future__ import absolute_import, unicode_literals

import clearbit
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from social_network import settings

UserModel = get_user_model()

logger = get_task_logger(__name__)


@shared_task(bind=True)
def fetch_user_data(self, user_id):
    try:
        target_user = UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        logger.exception("User for fetching additional data not found")
        return

    person = clearbit.Person.find(email=target_user.email, stream=True)

    if person is None:
        logger.warning("User not found on clearbit...retrying in 60s")
        raise self.retry(countdown=60, max_retries=settings.CLEARBIT_RETRIES)  # try again in a minute

    # had to use pop instead of get because of poor lib
    # that has overriden the dict's get, and i'm too lazy to do a PR right now
    target_user.full_name = target_user.full_name or person.pop('name', {}).pop('fullName', "")
    target_user.city = target_user.city or person.pop('geo', {}).pop('city', "")
    target_user.state = target_user.state or person.pop('geo', {}).pop('state', "")
    target_user.bio = target_user.bio or person.pop('bio', "")
    target_user.website = target_user.website or person.pop('site', "")
    target_user.github = target_user.github or person.pop('github', {}).pop('handle', "")

    target_user.save()
    return
