# Create your views here.
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import permissions, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from users.filters import UserFilter
from .serializers import UserSerializer


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


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
    pagination_class = UserPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_queryset(self):
        return get_user_model().objects.all().order_by('-id')
