from blog.models import Post, Comment
from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    created_before = filters.DateFilter(field_name="created_at", lookup_expr='lte')
    created_after = filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_exact = filters.DateFilter(field_name="created_at", lookup_expr='date')


    class Meta:
        model = Post
        fields = ['author', 'published']


class CommentFilter(filters.FilterSet):
    post = filters.ModelChoiceFilter(field_name='post', queryset=Post.objects.all())
    created_before = filters.DateFilter(field_name="created_at", lookup_expr='lte')
    created_after = filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_exact = filters.DateFilter(field_name="created_at", lookup_expr='date')

    class Meta:
        model = Comment
        fields = ['post']
