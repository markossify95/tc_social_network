# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.models import Post, Like
from core.serializers import PostSerializer, LikeSerializer


class PostPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    queryset = Post.objects.all()

    @action(detail=True, methods=['POST', 'DELETE'], url_name="like", url_path="like")
    def toggle_like(self, request, pk=None):
        user = request.user
        if request.method == "POST":
            serializer = LikeSerializer(data={'post': pk, 'user': user.id}, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                like = Like.objects.get(post_id=pk, user=user)
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Like.DoesNotExist as e:
                return Response(status=status.HTTP_404_NOT_FOUND)
