from django.contrib.auth.models import AbstractUser
from django.db import models


class NetworkUser(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(blank=False,
                                 null=False,
                                 max_length=300,
                                 help_text="Full name of network user.")
