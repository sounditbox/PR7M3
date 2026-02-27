import logging

from django.core.paginator import Paginator
from django.db.models import F
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

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
    context_object_name = 'posts' # default value: object_list
    paginate_by = 10

    def get_context_data(
        self, *, object_list = ..., **kwargs
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
    context_object_name = 'post' # default value: object
    pk_url_kwarg = 'post_id' # default value: pk

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

def post_list_paginated(request):
    # Важна сортировка!
    all_posts_qs = Post.objects.filter(published=True).order_by('-created_at')
    # 1. Создаем Paginator (10 постов на страницу)
    paginator = Paginator(all_posts_qs, 10)
    # 2. Получаем номер страницы из GET-параметра (?page=...)
    page_number = request.GET.get('page', 1)
    # 3. Получаем объект Page для нужной страницы
    page_obj = paginator.get_page(page_number)
    # 4. Передаем объект Page в контекст
    context = {'page_obj': page_obj}
    return render(request, 'post_list_paginated.html', context)