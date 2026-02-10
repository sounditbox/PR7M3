import logging

from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

posts_db = [{'id': 1, 'title': 'Post 1', 'content': 'My super interesting content'},
            {'id': 2, 'title': 'Post 2', 'content': 'My super interesting content!'},
            {'id': 3, 'title': 'Post 3', 'content': 'My super interesting content!!'}]


def post_list(request: HttpRequest) -> HttpResponse:
    logger.info(f'Post list requested: {request.path}')
    # логика работы с запросом
    posts_html = '<ul>'
    for p in posts_db:
        p['link'] = f'<a href={reverse('blog:post_detail', args=[p.get('id')])}>Details</a>'
        posts_html += f'<li>{p}</li>'
    posts_html += '</ul>'
    posts_html += f'<a href={reverse("blog:add_post")}>Add post</a>'
    return HttpResponse(f'<h1>All posts!</h1>{posts_html}')


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    logger.info(f'Post detail requested: {request.path}')
    logger.info(f'Query params: {request.GET}')
    for p in posts_db:
        if p.get('id') == post_id:
            return HttpResponse(
                f'<a href="{reverse('blog:post_list')}">Back to posts</a><h1>{p.get("title")}</h1> <p>{p.get("content")}</p> ')
    logger.error(f'Post {post_id} not found')
    return HttpResponse(f'<h1>Post {post_id}</h1> <p>Post not found</p>', status=404, headers={'X-Custom-Header': '42'})


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

@csrf_exempt
def add_post(request):
    logger.info('Adding post')
    html = (f'<h1>Add post</h1><form method="post">'
            f'<input type="text" name="title" placeholder="Title">'
            f'<input type="text" name="content" placeholder="Content">'
            f'<input type="submit" value="Add"></form>')
    if request.method == 'POST':
        title, content = request.POST.get('title'), request.POST.get('content')
        posts_db.append({'id': len(posts_db) + 1, 'title': title, 'content': content})
        return HttpResponse(
            f'<h1>Post added!</h1><a href="{reverse('blog:post_list')}">Back to posts</a>'
            f'<a href="{reverse('blog:add_post')}">Add another post</a>'
            f'<a href="{reverse('blog:post_detail', args=[len(posts_db)])}">Go to post</a>')
    return HttpResponse(html)


def year_archive(request: HttpRequest, year: int) -> HttpResponse:
    return HttpResponse(f'<h1>Year {year}</h1>')


def month_archive(request: HttpRequest, year: int, month: int) -> HttpResponse:
    return HttpResponse(f'<h1>Year {year}, Month {month}</h1>')
