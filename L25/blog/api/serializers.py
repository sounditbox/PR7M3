from blog.models import Post, Author, Tag, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']
        help_texts = {
            'id': 'Уникальный идентификатор пользователя.',
            'username': 'Имя пользователя.',
            'email': 'Адрес электронной почты.',
        }


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = '__all__'
        help_texts = {
            'user': 'Связанный объект модели User.',
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        help_texts = {
            'name': 'Название тега.',
            'slug': 'Уникальный идентификатор тега.',
            'color': 'Цвет тега.',
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at']
        help_texts = {
            'content': 'Текст комментария.',
            'post': 'Связанный объект модели Post.',
            'author': 'Связанный объект модели Author.',
            'created_at': 'Дата создания комментария.',
        }


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published', 'comments',
                  'author', 'created_at', 'updated_at', 'tags']
        read_only_fields = ['created_at', 'updated_at', 'views', 'id']
        help_texts = {
            'title': 'Название поста.',
            'content': 'Текст поста.',
            'published': 'Показывать ли пост пользователям.',
            'comments': 'Связанные объекты модели Comment.',
            'author': 'Связанный объект модели Author.',
            'created_at': 'Дата создания поста.',
            'updated_at': 'Дата обновления поста.',
            'tags': 'Связанные объекты модели Tag.',
        }

    def validate(self, attrs):
        title = attrs.get('title', getattr(self.instance, 'title', None))
        content = attrs.get('content', getattr(self.instance, 'content', None))
        if title == content:
            raise serializers.ValidationError("Заголовок и содержание должны быть разными.")
        return attrs


class ShortPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'published', 'author', 'created_at']
        read_only_fields = ['created_at', 'updated_at', 'views', 'id']
        help_texts = {
            'id': 'Уникальный идентификатор поста.',
            'title': 'Название поста.',
            'published': 'Показывать ли пост пользователям.',
            'author': 'Связанный объект модели Author.',
            'created_at': 'Дата создания поста.',
        }

    def to_representation(self, instance):
        instance.title = instance.title.upper()
        return super().to_representation(instance)