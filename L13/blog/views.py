import logging

from django.db.models import F
from django.db.models.aggregates import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .forms import FeedbackForm, PostForm, ExampleForm, StyledForm, CommentForm
from .models import Post

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(published=True).order_by('-created_at').annotate(comments_count=Count('comments'))
    template_name = 'post_list.html'
    context_object_name = 'posts'  # default value: object_list
    paginate_by = 10

    def get_context_data(
            self, *, object_list=..., **kwargs
    ) -> dict:
        context = super().get_context_data(**kwargs)
        context['stats'] = Post.objects.aggregate(
            total_posts=Count('id'),
            unique_authors=Count('author', distinct=True)
        )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'  # default value: object
    pk_url_kwarg = 'post_id'  # default value: pk

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create_update.html'
    # fields = ['title', 'content', 'tags', 'published']
    extra_context = {'title': 'Create Post'}
    success_url = reverse_lazy('blog:post_list')

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.author = request.user.author
    #     post.save()


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create_update.html'
    fields = ['title', 'content', 'tags', 'published']
    extra_context = {'title': 'Update Post'}
    success_url = reverse_lazy('blog:post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('blog:post_list')


class FeedbackView(FormView):
    form_class = StyledForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        logger.info('Feedback submitted: %s', form.cleaned_data)
        return super().form_valid(form)


def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'post_create_update.html', context={'form': form, 'title': 'Create Post'})
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user.author
        post.save()
        return redirect('blog:post_detail', post_id=post.pk)
    else:
        return render(request, 'post_create_update.html', context={'form': form, 'title': 'Create Post'})

@require_POST
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user.author
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)
    else:
        return render(request, reverse('blog:post_detail'), context={'form': form})
