from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer, ShortPostSerializer
from ..models import Post


# CRUD - Create Read Update Delete
# Retrieve List Create Update Destroy

class CreateListPostAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user.author)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request: Request) -> Response:
        posts = Post.objects.all()
        serializer = ShortPostSerializer(posts, many=True)
        return Response(serializer.data)


class RetrieveDeleteUpdatePostAPIView(APIView):
    def get(self, request: Request, pk: int) -> Response:
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # def put(self, request: Request, pk: int) -> Response:
    #     post = Post.objects.get(id=pk)
    #     serializer = PostSerializer(instance=post, )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)

    def delete(self, request: Request, pk: int) -> Response:
        post = Post.objects.get(id=pk)
        post.delete()
        return Response(status=204)
