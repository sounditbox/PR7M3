import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from blog.models import Post, Comment, Tag, Author


class PostObject(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


class AuthorObject(DjangoObjectType):
    class Meta:
        model = Author
        fields = '__all__'


class UserObject(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class CommentObject(DjangoObjectType):
    class Meta:
        model = Comment
        fields = '__all__'


class TagObject(DjangoObjectType):
    class Meta:
        model = Tag
        fields = '__all__'


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)


class PostConnection(graphene.relay.Connection):
    class Meta:
        node = PostNode


class BlogQuery(graphene.ObjectType):
    post = graphene.relay.Node.Field()
    posts_paginated = graphene.relay.ConnectionField(PostConnection)

    all_posts = graphene.List(PostObject)
    get_post = graphene.Field(PostObject, id=graphene.ID())

    all_comments = graphene.List(CommentObject)
    get_comment = graphene.Field(CommentObject, id=graphene.ID())

    get_comments_by_post = graphene.List(CommentObject, post_id=graphene.ID())

    def resolve_posts_paginated(self, info, first=None, after=None, last=None, before=None):
        return Post.objects.all()

    def resolve_all_posts(self, info):
        return Post.objects.all().prefetch_related('comments', 'author', 'tags')

    def resolve_get_post(self, info, id):
        return Post.objects.get(id=id)

    def resolve_get_comments_by_post(self, info, post_id):
        return Comment.objects.filter(post_id=post_id)

    def resolve_all_comments(self, info):
        return Comment.objects.all()

    def resolve_get_comment(self, info, id):
        return Comment.objects.get(id=id)


class CreatePostMutation(graphene.Mutation):
    # данные от клиента
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        tag_ids = graphene.List(graphene.ID)

    # возврат значений
    post = graphene.Field(PostObject)

    @staticmethod
    def mutate(root, info, title, content, tag_ids):
        # валидация данных
        if not title or not content:
            raise Exception("Title and content are required")
        # if not info.context.user.is_authenticated:
        #     raise Exception("User is not authenticated")

        # создание поста
        post = Post.objects.create(title=title, content=content)
        if tag_ids:
            post.tags.set(tag_ids)
        post.save()

        return CreatePostMutation(post=post)


class UpdatePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        content = graphene.String()
        tag_ids = graphene.List(graphene.ID)

    # возврат значений
    post = graphene.Field(PostObject)

    @staticmethod
    def mutate(root, info, id, title, content, tag_ids):
        post = Post.objects.get(id=id)
        # валидация данных
        if title:
            post.title = title
        if content:
            post.content = content
        if tag_ids:
            post.tags.set(tag_ids)
        # if not info.context.user.is_authenticated:
        #     raise Exception("User is not authenticated")
        post.save()
        return CreatePostMutation(post=post)


class DeletePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        if Post.objects.filter(id=id).exists():
            Post.objects.get(id=id).delete()
            return DeletePostMutation(ok=True)
        return DeletePostMutation(ok=False)
