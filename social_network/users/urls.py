from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import CreateUserView

router = SimpleRouter()

router.register('register', CreateUserView, base_name='register')

urlpatterns = [
    url(r'^auth/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^auth/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
