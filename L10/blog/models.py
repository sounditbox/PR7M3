from django.contrib.auth import get_user_model
from django.db import models


class Author(models.Model):
    # id
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    # posts: Manager(Post.filter(author=self.id))

    def __str__(self):
        return self.user.username

class Post(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='posts')
    comment_authors = models.ManyToManyField(Author, through='Comment')

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'id:{self.id}, {self.title}'


class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


class Tag(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.name