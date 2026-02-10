from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)

    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'id:{self.id}, {self.title}'
