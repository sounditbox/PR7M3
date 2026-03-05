import logging

from django.db.models import F
from django.db.models.aggregates import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .forms import FeedbackForm, PostForm, ExampleForm, StyledForm
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


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create_update.html'
    fields = ['title', 'content']
    extra_context = {'title': 'Create Post'}
    success_url = reverse_lazy('blog:post_list')


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create_update.html'
    fields = ['title', 'content']
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
        print(form.cleaned_data)
        return super().form_valid(form)


def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'post_create_update.html', context={'form': form, 'title': 'Create Post'})
    form = PostForm(request.POST)
    if form.is_valid():
        post = Post(**form.cleaned_data)
        post.author = request.user.author
        post.save()
        return redirect('blog:post_list')
    else:
        return render(request, 'post_create_update.html', context={'form': form, 'title': 'Create Post'})

