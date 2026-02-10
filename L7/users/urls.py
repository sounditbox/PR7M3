from django.urls import path, re_path

from .views import year_archive

app_name = 'users'

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/$', year_archive, name='year_archive'),
    ]