import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.db.models.aggregates import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .forms import PostForm, StyledForm, CommentForm
from .mixins import ErrorMessageMixin, AuthorRequiredMixin
from .models import Post, Comment, Author

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


class PostListView(PermissionRequiredMixin, ListView):
    model = Post
    queryset = Post.objects.filter(published=True).order_by('-created_at').annotate(comments_count=Count('comments'))
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  # default value: object_list
    paginate_by = 10
    permission_required = ['blog.view_post']

    def get_context_data(
            self, *, object_list=..., **kwargs
    ) -> dict:
        context = super().get_context_data(**kwargs)
        context['stats'] = Post.objects.aggregate(
            total_posts=Count('id'),
            unique_authors=Count('author', distinct=True)
        )
        return context


class PostDetailView(PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # default value: object
    pk_url_kwarg = 'post_id'  # default value: pk
    permission_required = ['blog.view_post']

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


# MRO - method resolution order
class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create_update.html'
    extra_context = {'title': 'Create Post'}
    success_message = 'Пост успешно создан!'
    error_message = 'При создании поста что-то пошло не так:('
    permission_required = ['blog.add_post']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author, _ = Author.objects.get_or_create(user=self.request.user)
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    model = Post
    template_name = 'blog/post_create_update.html'
    fields = ['title', 'content', 'tags', 'published']
    extra_context = {'title': 'Update Post'}
    success_message = 'Пост успешно обновлён'
    error_message = 'При обновлении поста что-то пошло не так:('
class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, ErrorMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')
    success_message = 'Пост успешно удалён'
class FeedbackView(FormView):
    form_class = StyledForm
    template_name = 'blog/feedback.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        logger.info('Feedback submitted: %s', form.cleaned_data)
        return super().form_valid(form)


@login_required
@permission_required('blog.add_post')
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/post_create_update.html', context={'form': form, 'title': 'Create Post'})
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author, _ = Author.objects.get_or_create(user=request.user)
        post.save()
        form.save_m2m()
        messages.success(request, 'Пост успешно создан!')
        return redirect('blog:post_detail', post_id=post.pk)
    else:
        messages.error(request, 'При создании поста что-то пошло не так:(', 'danger')
        return render(request, 'blog/post_create_update.html', context={'form': form, 'title': 'Create Post'})


@login_required
@require_POST
@permission_required('blog.add_comment')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author, _ = Author.objects.get_or_create(user=request.user)
        comment.post = post
        comment.save()
        messages.success(request, 'Комментарий добавлен!')
        return redirect('blog:post_detail', post_id=post_id)
    else:
        messages.error(request, 'При создании комментария что-то пошло не так:(')
        return render(request, 'blog/post_detail.html', context={'post': post, 'form': form})


class CommentDeleteView(LoginRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    success_message = 'Комментарий успешно удалён'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.post.pk})
