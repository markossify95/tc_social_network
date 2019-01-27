from rest_framework.routers import SimpleRouter

from core.views import PostViewSet

router = SimpleRouter()

router.register('posts', PostViewSet, base_name='posts')

urlpatterns = []

urlpatterns += router.urls
