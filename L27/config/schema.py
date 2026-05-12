import graphene
from blog.schema import (BlogQuery, CreatePostMutation,
                         UpdatePostMutation, DeletePostMutation)


class Query(BlogQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
