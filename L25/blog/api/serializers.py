from blog.models import Post, Author, Tag, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published', 'comments',
                  'author', 'created_at', 'updated_at', 'tags']
        read_only_fields = ['created_at', 'updated_at', 'views', 'id']

    def validate(self, attrs):
        title = attrs.get('title', getattr(self.instance, 'title', None))
        content = attrs.get('content', getattr(self.instance, 'content', None))
        if title == content:
            raise serializers.ValidationError("Title and content must be different.")
        return attrs


class ShortPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'published', 'author', 'created_at']
        read_only_fields = ['created_at', 'updated_at', 'views', 'id']

    def to_representation(self, instance):
        instance.title = instance.title.upper()
        return super().to_representation(instance)
