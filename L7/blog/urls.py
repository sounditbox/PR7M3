from django.urls import path, re_path

from .views import contacts, SimpleView, PostListView, PostDetailView, \
    PostCreateView, PostUpdateView, PostDeleteView  # post_list, add_post, post_detail


app_name = 'blog'

urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('add_post/', PostCreateView.as_view(), name='add_post'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('simple/', SimpleView.as_view(), name='simple'),
]
