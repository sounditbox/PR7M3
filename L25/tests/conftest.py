import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from blog.models import Post, Author


# fixture - заготовленные заранее данные

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = get_user_model().objects.create(
        username='testuser',
        password='testpass',
        is_staff=True,
    )
    Author.objects.create(user=user)
    return user


@pytest.fixture
def another_user():
    user = get_user_model().objects.create(
        username='testuser2',
        password='testpass2',
        is_staff=False
    )
    Author.objects.create(user=user)
    return user


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def post(user):
    return Post.objects.create(
        title='Test Post',
        content='This is a test post.',
        author=Author.objects.get(user=user)
    )


@pytest.fixture
def post_data():

    return {
        'title': 'Test Post',
        'content': 'This is a new data for post',
    }


@pytest.fixture
def post_invalid_data():

    return {
        'title': 42,
    }
