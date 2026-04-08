# blog/urls.py
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views  # Импортируем наши API views

app_name = 'blog_api'  # Задаем namespace

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('comments', views.CommentViewSet, basename='comment')



urlpatterns = [
    path('posts/', views.CreateListPostAPIView.as_view(), name='create_list_post'),
    path('posts/<int:pk>/', views.RetrieveDeleteUpdatePostAPIView.as_view(), name='retrieve_delete_update_post'),

    path('generics/posts/', views.ListCreatePostView.as_view(), name='list_create_post'),
    path('generics/posts/<int:pk>/', views.RetrieveUpdateDestroyPostView.as_view(),
         name='retrieve_update_destroy_post'),

    path('viewsets/', include(router.urls)),


    path('token-auth/', obtain_auth_token),  # TokenAuth

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWTAuth
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
