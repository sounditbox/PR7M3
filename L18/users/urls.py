from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from .views import LoginUserView, CreateUserView, ProfileView, UpdateUserView

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        next_page=reverse_lazy('blog:post_list')
    ), name='logout'),

    # path('login/', login_user, name='login') fbv solution
    path('login/', LoginUserView.as_view(), name='login'),  # cbv solution
    # path('login/', LoginView.as_view(
    #     redirect_authenticated_user=True,
    #     next_page=reverse_lazy('blog:post_list')
    # ), name='login')

    path('register/', CreateUserView.as_view(), name='register'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='user_update'),

    path('password-reset', PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/custom_password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/custom_password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/custom_password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='registration/custom_password_reset_complete.html'
    ), name='password_reset_complete'),

    path('password-change/', PasswordChangeView.as_view(
        template_name='registration/custom_password_change.html',
        success_url=reverse_lazy('users:password_change_done')
    ), name='password_change'),

    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/custom_password_change_done.html'
    ), name='password_change_done')

]
