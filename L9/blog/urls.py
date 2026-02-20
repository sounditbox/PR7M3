from django.urls import path

from .views import PostListView, PostDetailView, \
    PostCreateView, PostUpdateView, PostDeleteView, post_list_paginated  # post_list, add_post, post_detail

app_name = 'blog'

urlpatterns = [
    path('posts/create', PostCreateView.as_view(), name='add_post'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts_paginated', post_list_paginated)
]
