import logging

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


# def post_list(request: HttpRequest) -> HttpResponse:
#     logger.info(f'Post list requested: {request.path}')
#     # логика работы с запросом
#     posts_html = '<ul>'
#     for p in Post.objects.all():
#         p['link'] = f'<a href={reverse('blog:post_detail', args=[p.id])}>Details</a>'
#         posts_html += f'<li>{p}</li>'
#     posts_html += '</ul>'
#     posts_html += f'<a href={reverse("blog:add_post")}>Add post</a>'
#     return HttpResponse(f'<h1>All posts!</h1>{posts_html}')

# class PostListView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'post_list.html', {'posts': Post.objects.all()})

# class PostListView(TemplateView):
#     extra_context = {'posts': Post.objects.all()}
#     template_name = 'post_list.html'

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts' # default value: object_list


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post' # default value: object
    pk_url_kwarg = 'post_id' # default value: pk

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




# def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
#     logger.info(f'Post detail requested: {request.path}')
#     logger.info(f'Query params: {request.GET}')
#     for p in posts_db:
#         if p.get('id') == post_id:
#             return HttpResponse(
#                 f'<a href="{reverse('blog:post_list')}">Back to posts</a><h1>{p.get("title")}</h1> <p>{p.get("content")}</p> ')
#     logger.error(f'Post {post_id} not found')
#     return HttpResponse(f'<h1>Post {post_id}</h1> <p>Post not found</p>', status=404, headers={'X-Custom-Header': '42'})


@csrf_exempt
def contacts(request: HttpRequest) -> HttpResponse:
    logger.info(f'Contacts requested: {request.path}')
    logger.info(f'Body params: {request.POST}')
    html = (f'<h1>Contacts</h1><form method="post">'
            f'<h2>Leave us your message</h2>'
            f'<input type="text" name="name" placeholder="Name">'
            f'<input type="text" name="message" placeholder="Message">'
            f'<input type="email" name="email" placeholder="Your Email">'
            f'<input type="submit" value="Send"></form>')
    return HttpResponse(html)

class ContactsView(View):
    pass

class SimpleView(View):
    message = "Default message from SimpleView"


    def get(self, request, *args, **kwargs):
        return render(request, 'simple.html', {'message': self.message, 'method': 'get'})

    def post(self, request, *args, **kwargs):
        self.message = request.POST.get('message')
        return render(request, 'simple.html', {'message': self.message, 'method': 'post'})


# @csrf_exempt
# def add_post(request):
#     logger.info('Adding post')
#     html = (f'<h1>Add post</h1><form method="post">'
#             f'<input type="text" name="title" placeholder="Title">'
#             f'<input type="text" name="content" placeholder="Content">'
#             f'<input type="submit" value="Add"></form>')
#     if request.method == 'POST':
#         title, content = request.POST.get('title'), request.POST.get('content')
#         posts_db.append({'id': len(posts_db) + 1, 'title': title, 'content': content})
#         return HttpResponse(
#             f'<h1>Post added!</h1><a href="{reverse('blog:post_list')}">Back to posts</a>'
#             f'<a href="{reverse('blog:add_post')}">Add another post</a>'
#             f'<a href="{reverse('blog:post_detail', args=[len(posts_db)])}">Go to post</a>')
#     return HttpResponse(html)