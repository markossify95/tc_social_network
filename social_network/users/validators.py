from pyhunter import PyHunter
from rest_framework import serializers

from social_network import settings


class HunterEmailValidator:
    def __call__(self, value):  # we must run email validation synchronously
        try:
            hunter = PyHunter(settings.HUNTER_API_KEY)
            resp_data = hunter.email_verifier(value)
        except Exception as e:
            message = "Failed to validate email. Please, try later."
            raise serializers.ValidationError(message)

        if resp_data.get('score') < settings.HUNTER_VALIDATION_TRESHOLD:
            message = "Invalid email."
            raise serializers.ValidationError(message)
