from django.urls import path, re_path

from .views import post_list, post_detail, year_archive, month_archive, contacts, add_post

app_name = 'blog'

urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('add_post/', add_post, name='add_post'),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', year_archive, name='year_archive'),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', month_archive),
]
