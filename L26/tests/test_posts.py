import pytest
from django.urls import reverse

from blog.models import Post
from blog.api.serializers import PostSerializer
from rest_framework import status

from rest_framework.test import APIClient


def test_get_post_success(db, api_client, post):
    response = api_client.get(
        reverse('api:post-detail', kwargs={'pk': post.id}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == post.title
    assert response.data['content'] == post.content


def test_get_post_fail(db, api_client, post):
    response = api_client.get(
        reverse('api:post-detail', kwargs={'pk': 42}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Post matches the given query.'


def test_get_posts(db, api_client, post):
    response = api_client.get(reverse('api:post-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['data'][0]['title'] == post.title.upper()


def test_create_post_success(db, auth_client, user, post_data):
    auth_client.post(reverse('api:post-list'), data=post_data)
    assert Post.objects.count() == 1
    assert Post.objects.first().title == 'Test Post'
    assert Post.objects.first().content == 'This is a test post.'
    assert Post.objects.first().author.user == user


def test_create_post_fail(db, auth_client, user):
    response = APIClient().post(reverse('api:post-list'), data={
        'title': 'Test Post',
        'content': 'This is a test post.',
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Post.objects.count() == 0
    assert response.data['detail'] == 'Учетные данные не были предоставлены.'


def test_update_post_success(db, auth_client, user, post, post_data):
    response = auth_client.patch(reverse('api:post-detail',
                                         args=(1,)),
                                 data=post_data)
    assert Post.objects.count() == 1
    assert Post.objects.first().title == post_data['title']
    assert Post.objects.first().content == post_data['content']
    assert Post.objects.first().author.user == user
    assert response.status_code == status.HTTP_200_OK


def test_update_post_fail_401(db, api_client, post, post_data):
    response = APIClient().patch(reverse('api:post-detail',
                                         args=(post.id,)),
                                 data=post_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Post.objects.count() == 1
    assert response.data['detail'] == 'Учетные данные не были предоставлены.'


def test_update_post_fail_403(db, api_client, user, post, post_data,
                              another_user):
    api_client.force_authenticate(user=another_user)
    response = api_client.patch(
        reverse('api:post-detail', args=(post.id,)), data=post_data)
    unchanged_post = Post.objects.get(id=post.id)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert unchanged_post.title == post.title
    assert unchanged_post.content == post.content


def test_delete_post_success(db, auth_client, post):
    response = auth_client.delete(
        reverse('api:post-detail', kwargs={'pk': post.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Post.objects.count() == 0


def test_delete_post_fail(db, api_client):
    response = api_client.delete(
        reverse('api:post-detail', kwargs={'pk': 42}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'No Post matches the given query.'


def test_post_serializer(db, post_data):
    ser = PostSerializer(data=post_data)
    assert ser.is_valid()
    assert ser.validated_data == post_data


def test_post_serializer_invalid(db, post_invalid_data):
    ser = PostSerializer(data=post_invalid_data)
    assert not ser.is_valid()
    assert 'content' in ser.errors
