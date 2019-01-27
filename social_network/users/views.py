# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import permissions, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer


class CreateUserView(CreateAPIView, GenericViewSet):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class UsersViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
