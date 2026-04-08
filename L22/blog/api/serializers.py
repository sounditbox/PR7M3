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


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published', 'comments',
                  'author', 'created_at', 'updated_at', 'tags']
        # exclude = ['content', 'author']
        read_only_fields = ['created_at', 'updated_at', 'views', 'id']

        # extra_kwargs = {'published': {'read_only': True}}

    def validate(self, attrs):
        if attrs['title'] == attrs['content']:
            raise serializers.ValidationError("Название и содержимое не могут быть одинаковыми.")
        return attrs

class ShortPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published', 'author', 'created_at']
        read_only_fields = ['created_at', 'updated_at', 'views', 'id']

    def to_representation(self, instance):
        instance.title = instance.title.upper()
        return super().to_representation(instance)

# class CommentSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     content = serializers.CharField(max_length=1000)
#     created_at = serializers.DateTimeField(read_only=True)
#     post_id = serializers.IntegerField(write_only=True, required=True)
#     author_id = serializers.IntegerField(write_only=True, required=True)
#
#     def validate_content(self, value):
#         if "плохоеслово" in value.lower():
#             raise serializers.ValidationError("Комментарий содержит плохие слова.")
#         return value
