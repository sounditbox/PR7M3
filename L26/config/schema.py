import graphene
from blog.schema import BlogQuery


class Query(BlogQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query) # mutation=BlogMutation
