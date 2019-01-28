from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.tasks import fetch_user_data
from users.validators import HunterEmailValidator

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=UserModel.objects.all()), HunterEmailValidator()])

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel.objects.create(
            **validated_data
        )
        user.set_password(password)
        user.save()
        fetch_user_data.delay(user.id)
        return user

    class Meta:
        model = UserModel
        fields = (
            "id", "username", "password", "email", "full_name", "bio", "city", "state", "github", "website",
            "like_count", "has_unpopular_posts")


class DetailedUserSerializer(serializers.ModelSerializer):
    from core.serializers import SkinnyPostSerializer
    posts = SkinnyPostSerializer(many=True, source='post_set')

    class Meta:
        model = UserModel
        fields = (
            "id", "username", "password", "email", "full_name", "bio", "city", "state", "github", "website",
            "like_count", "posts", "has_unpopular_posts")
