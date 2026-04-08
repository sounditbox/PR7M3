# blog/urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views # Импортируем наши API views

app_name = 'blog_api'  # Задаем namespace
urlpatterns = [
   # path('posts/', views.PostListCreateAPI.as_view(), name='post_list_create'),
   # path('posts/<int:pk>/', views.PostDetailAPI.as_view(), name='post_detail'),
   # path('posts/<int:post_pk>/comments/', views.CommentListAPI.as_view(), name='comment_list'),
    path('posts/', views.CreateListPostAPIView.as_view(), name='create_post'),
    path('posts/<int:pk>/', views.RetrieveDeleteUpdatePostAPIView.as_view(), name='create_post'),

    path('token-auth/', obtain_auth_token), # TokenAuth

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # JWTAuth
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

