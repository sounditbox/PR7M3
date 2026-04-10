from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthorOrReadOnly, IsAuthor
from .serializers import PostSerializer, ShortPostSerializer, CommentSerializer
from ..models import Post, Author, Comment


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


class RetrieveUpdateDestroyPostView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

class ListCreatePostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author, _ = Author.objects.get_or_create(user=self.request.user)
        serializer.save(author=author)


class PostViewSet(viewsets.ModelViewSet):
    """API эндпоинт, предоставляющий полный CRUD для постов."""
    queryset = Post.objects.filter(published=True).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]
    # authentication_classes = []

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthor()]

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortPostSerializer
        return PostSerializer

    @action(detail=True, methods=['post'], url_path='publish', url_name='publish',
            permission_classes=[IsAuthor], queryset=Post.objects.filter(published=False))
    def publish(self, request, pk):
        post = self.get_object()
        post.published = True
        post.save(update_fields=['published'])
        return Response({'message': 'Post published successfully'}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.queryset.filter(post=self.request.query_params['post_id'])

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthor()]
