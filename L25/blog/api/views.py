from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, \
    IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PostFilter, CommentFilter
from .pagination import PostPagination, CommentPagination
from .permissions import IsAuthorOrReadOnly, IsAuthor
from .serializers import PostSerializer, ShortPostSerializer, CommentSerializer
from ..models import Post, Author, Comment


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
        author, _ = Author.objects.get(user=self.request.user)
        serializer.save(author=author)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = [
        'title',
        'content',
        'author__user__username',
        '^author__user__email'
    ]
    ordering_fields = ['created_at', 'published', 'author_id']

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('comments')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]

    def perform_create(self, serializer):
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortPostSerializer
        return PostSerializer

    @action(detail=True, methods=['post'], url_path='publish', url_name='publish',
            permission_classes=[IsAuthor])
    def publish(self, request, pk):
        post = self.get_object()
        if post.published:
            return Response({'message': 'Post is already published'}, status=400)
        post.published = True
        post.save(update_fields=['published'])
        return Response({'message': 'Post published successfully'}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['content', 'post__title', 'post__content']
    ordering_fields = ['created_at', 'post']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthor()]

    def perform_create(self, serializer):
        author = Author.objects.get_or_create(user=self.request.user)
        serializer.save(author=author)
