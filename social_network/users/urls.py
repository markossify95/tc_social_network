from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import CreateUserView, UsersViewSet

router = DefaultRouter()

router.register('register', CreateUserView, base_name='register')
router.register('users', UsersViewSet, base_name='users')

urlpatterns = [
    url(r'^auth/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^auth/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]

# urlpatterns += router.urls
