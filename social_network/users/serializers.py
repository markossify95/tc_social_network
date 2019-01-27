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
        print("Starting the task for user with id:", user.id)
        fetch_user_data.delay(user.id)
        return user

    class Meta:
        model = UserModel
        fields = (
            "id", "username", "password", "email", "full_name", "bio", "city", "state", "github", "website",
            "likes_count",)
