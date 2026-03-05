from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Post(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Содержимое')

    published = models.BooleanField(default=False, verbose_name='Опубликовано')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='posts',
                               verbose_name='Автор')

    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    tags = models.ManyToManyField('Tag', null=True, blank=True, related_name='posts', verbose_name='Теги')

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})

    def __str__(self):
        return f'Post: {self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'



class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')


    def __str__(self):
        return f'{self.author} | {self.post} - {self.content}'


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'