import graphene
from graphene_django import DjangoObjectType

from blog.models import Post, Comment, Tag


class PostObject(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


class CommentObject(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'


class TagObject(DjangoObjectType):
    class Meta:
        model = Tag
        fields = '__all__'


class BlogQuery(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")

    all_posts = graphene.List(PostObject)
    get_post = graphene.Field(PostObject, id=graphene.ID())

    all_comments = graphene.List(CommentObject)
    get_comment = graphene.Field(CommentObject, id=graphene.ID())

    get_comments_by_post = graphene.List(CommentObject, post_id=graphene.ID())

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_get_post(self, info, id):
        return Post.objects.get(id=id)

    def resolve_get_comments_by_post(self, info, post_id):
        return Comment.objects.filter(post_id=post_id)

    def resolve_all_comments(self, info):
        return Comment.objects.all()

    def resolve_get_comment(self, info, id):
        return Comment.objects.get(id=id)

# class BlogMutation(graphene.Mutation):
#     pass
