from django.contrib.auth.models import AbstractUser
from django.db import models


class NetworkUser(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(blank=True,
                                 null=True,
                                 max_length=300,
                                 help_text="Full name of network user.")
    city = models.CharField(blank=True,
                            null=True,
                            max_length=100,
                            help_text="User's city.")
    state = models.CharField(blank=True,
                             null=True,
                             max_length=100,
                             help_text="User's state.")
    bio = models.TextField(blank=True,
                           null=True,
                           max_length=1000,
                           help_text="User's bio.")

    website = models.CharField(blank=True,
                               null=True,
                               max_length=300,
                               help_text="User's website url.")
    github = models.CharField(blank=True,
                              null=True,
                              max_length=100,
                              help_text="User's github account name.")
