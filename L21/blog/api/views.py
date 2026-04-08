from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, ShortPostSerializer
from ..models import Post, Author


# CRUD - Create Read Update Delete
# Retrieve List Create Update Destroy

class CreateListPostAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request) -> Response:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            author, _ = Author.objects.get_or_create(user=request.user)
            serializer.save(author=author)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request: Request) -> Response:
        posts = Post.objects.all()
        serializer = ShortPostSerializer(posts, many=True)
        return Response(serializer.data)


class RetrieveDeleteUpdatePostAPIView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request: Request, pk: int) -> Response:
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request: Request, pk: int) -> Response:
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=204)
