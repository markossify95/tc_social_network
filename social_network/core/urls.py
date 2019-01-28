from rest_framework.routers import DefaultRouter

from core.views import PostViewSet

router = DefaultRouter()

router.register('posts', PostViewSet, base_name='posts')

urlpatterns = []

urlpatterns += router.urls
