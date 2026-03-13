from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import login_user, LoginUserView

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy('blog:post_list')
    ), name='logout'),

    # path('login/', login_user, name='login') fbv solution

    path('login/', LoginUserView.as_view(), name='login') # cbv solution

    # path('login/', LoginView.as_view(
    #     redirect_authenticated_user=True,
    #     next_page=reverse_lazy('blog:post_list') # TODO: change to profile view
    # ), name='login')
]
