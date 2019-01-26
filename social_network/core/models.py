from django.contrib.auth import get_user_model
from django.db import models


class AbstractModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, help_text="Time when object was created.")
    updated = models.DateTimeField(auto_now=True, help_text="Last time of object update.")

    class Meta:
        abstract = True


class Post(AbstractModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False, blank=False)
    content = models.TextField(max_length=1000, null=False, blank=False)
    likers = models.ManyToManyField(get_user_model(), through='Like', related_name='likers')
    like_count = models.PositiveIntegerField(default=0)


class Like(AbstractModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
