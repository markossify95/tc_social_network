from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.mixins import PasteUserMixin
from core.models import Post, Like
from users.serializers import UserSerializer

UserModel = get_user_model()


class PostField(serializers.RelatedField):
    def run_validation(self, data=serializers.empty):
        if data == serializers.empty:
            return super().run_validation(data)
        try:
            Post.objects.get(id=data)
        except Post.DoesNotExist as e:
            self.fail('invalid_post_id')
        return super().run_validation(data)

    def to_internal_value(self, data):
        return Post.objects.get(id=data)

    def to_representation(self, value):
        return {'id': value.id, 'title': value.title}

    def get_queryset(self):
        return Post.objects.all()

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([(item.id, "{}".format(item.title)) for item in queryset])


class PostSerializer(PasteUserMixin, serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    likers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'content', 'likers', 'like_count',)


class SkinnyPostSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    likers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'likers', 'like_count',)


class LikeSerializer(PasteUserMixin, serializers.ModelSerializer):
    post = PostField(error_messages={'invalid_post_id': 'Given post does not exist.'})
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('user', 'post',)

    def validate(self, attrs):
        super().validate(attrs)
        if Like.objects.filter(post=attrs['post'], user=attrs['user']).exists():
            raise ValidationError(detail="You have already liked this post")

        if attrs['post'].user == attrs['user']:
            raise ValidationError(detail="You can not like your own post")

        return attrs
