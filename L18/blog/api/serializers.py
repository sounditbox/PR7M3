from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ['id', 'title', 'content', 'published', 'author', 'created_at', 'updated_at']
        exclude = ['tags']
        read_only_fields = ['author', 'created_at', 'updated_at', 'views', 'id']
        # extra_kwargs = {'published': {'read_only': True}}




class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(max_length=1000)
    created_at = serializers.DateTimeField(read_only=True)
    post_id = serializers.IntegerField(write_only=True, required=True)
    author_id = serializers.IntegerField(write_only=True, required=True)

    def validate_content(self, value):
        if "плохоеслово" in value.lower():
            raise serializers.ValidationError("Комментарий содержит плохие слова.")
        return value
