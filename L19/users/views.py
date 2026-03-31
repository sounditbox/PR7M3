from blog.models import Author
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, CreateView, TemplateView, UpdateView

from .forms import UserUpdateForm, UserCreateForm


# fbv for AuthN
@require_http_methods(['GET', 'POST'])
def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect(reverse_lazy('blog:post_list'))
        else:
            return render(request, 'registration/login.html', {'form': form})


class LoginUserView(FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form: AuthenticationForm):
        login(request=self.request, user=form.user_cache)
        Author.objects.get_or_create(user=self.request.user)
        messages.success(self.request, 'Login success!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Login failed!')
        return super().form_invalid(form)


class CreateUserView(CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        Author.objects.get_or_create(user=self.object)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author, _ = Author.objects.get_or_create(user=self.request.user)
        context['form'] = UserUpdateForm(instance=self.request.user)
        context['posts'] = author.posts.all()
        context['comments'] = author.comments.all()
        return context


class UpdateUserView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')
    # template_name = 'users/profile.html'
