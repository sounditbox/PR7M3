import pytest
from django.urls import reverse

from blog.models import Post


@pytest.mark.django_db
def test_get_post_success(api_client, post):
    response = api_client.get(
        reverse('api:post-detail', kwargs={'pk': post.id}))
    assert response.status_code == 200
    assert response.data['title'] == post.title
    assert response.data['content'] == post.content


@pytest.mark.django_db
def test_get_post_fail(api_client, post):
    response = api_client.get(
        reverse('api:post-detail', kwargs={'pk': 42}))
    assert response.status_code == 404
    assert response.data['detail'] == 'No Post matches the given query.'


@pytest.mark.django_db
def test_get_posts(api_client, post):
    response = api_client.get(reverse('api:post-list'))
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['data'][0]['title'] == post.title.upper()


@pytest.mark.django_db
def test_create_post(auth_client, user):
    auth_client.post(reverse('api:post-list'), data={
        'title': 'Test Post',
        'content': 'This is a test post.',
    })
    assert Post.objects.count() == 1
    assert Post.objects.first().title == 'Test Post'
    assert Post.objects.first().content == 'This is a test post.'
    assert Post.objects.first().author.user == user


@pytest.mark.django_db
def test_update_post_success(auth_client, user):
    auth_client.post(reverse('api:post-list'), data={
        'title': 'Test Post',
        'content': 'This is a test post.',
    })
    assert Post.objects.count() == 1
    assert Post.objects.first().title == 'Test Post'
    assert Post.objects.first().content == 'This is a test post.'
    assert Post.objects.first().author.user == user


@pytest.mark.django_db
def test_update_post_fail(api_client):
    response = api_client.post(reverse('api:post-list'), data={
        'title': 'Test Post',
        'content': 'This is a test post.',
    })
    assert response.status_code == 401
    assert Post.objects.count() == 0


@pytest.mark.django_db
def test_delete_post_success(auth_client, post):
    response = auth_client.delete(
        reverse('api:post-detail', kwargs={'pk': post.id}))
    assert response.status_code == 204
    assert Post.objects.count() == 0


@pytest.mark.django_db
def test_delete_post_fail(api_client):
    response = api_client.delete(
        reverse('api:post-detail', kwargs={'pk': 42}))
    assert response.status_code == 404
    assert response.data['detail'] == 'No Post matches the given query.'
