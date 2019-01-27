from pyhunter import PyHunter
from rest_framework import serializers

from social_network import settings


class HunterEmailValidator:
    def __call__(self, value):  # we must run email validation synchronously
        try:
            hunter = PyHunter(settings.HUNTER_API_KEY)
            resp_data = hunter.email_verifier(value)
            if resp_data['result'] != 'deliverable':
                message = "Invalid email."
                raise serializers.ValidationError(message)
        except:
            message = "Failed to validate email. Please, try later."
            raise serializers.ValidationError(message)
