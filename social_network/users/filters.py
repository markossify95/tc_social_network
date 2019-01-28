from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters import rest_framework as filters


class OrderByPostsCountFilter(filters.OrderingFilter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('posts_count', 'Number of posts by any user (ASC)'),
            ('-posts_count', 'Number of posts by any user (ASC)'),
        ]

    def filter(self, qs, value):
        if not value:
            return qs

        if 'posts_count' in value:
            qs = qs.annotate(posts_count=Count('post', distinct=True)).order_by('posts_count')
            return qs

        elif '-posts_count' in value:
            qs = qs.annotate(posts_count=Count('post', distinct=True)).order_by('-posts_count')
            return qs

        return super().filter(qs, value)


class UserFilter(filters.FilterSet):
    likes__lt = filters.NumberFilter(method='filter_by_like_count', label='max number of likes (excluding)')
    order_by = OrderByPostsCountFilter()

    def filter_by_like_count(self, queryset, name, value):
        queryset = queryset.annotate(num_likes=Count('like', distinct=True)).filter(num_likes__lt=value)
        return queryset

    class Meta:
        model = get_user_model()
        fields = []
