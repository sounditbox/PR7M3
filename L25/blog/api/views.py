from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, \
    OpenApiResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
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
    """
    View for creating and listing posts.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request) -> Response:
        """
        Create a new post.
        """
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            author, _ = Author.objects.get_or_create(user=request.user)
            serializer.save(author=author)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request: Request) -> Response:
        """
        List all posts.
        """
        posts = Post.objects.all()
        serializer = ShortPostSerializer(posts, many=True)
        return Response(serializer.data)


class RetrieveDeleteUpdatePostAPIView(APIView):
    """
    View for retrieving, updating and deleting posts.
    """
    permission_classes = [IsAuthorOrReadOnly]

    def get(self, request: Request, pk: int) -> Response:
        """
        Retrieve a post by its ID.
        """
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        """
        Update a post by its ID.
        """
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request: Request, pk: int) -> Response:
        """
        Delete a post by its ID.
        """
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=204)


class RetrieveUpdateDestroyPostView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]


class ListCreatePostView(ListCreateAPIView):
    """
    View for creating and listing posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)


class PostViewSet(viewsets.ModelViewSet):
    """
    View set for Post model.

    This viewset provides endpoints for creating, listing, retrieving and
    updating posts. It also includes a custom endpoint for publishing a post.
    """

    queryset = Post.objects.select_related('author').prefetch_related(
        'comments')
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

    @extend_schema(
        summary="Список постов с фильтром",
        description="Возвращает список постов. Можно фильтровать по `is_published`.",
        # Добавляем описание query-параметра
        parameters=[
            OpenApiParameter(name='is_published', type=bool,
                             description='Filter by published status')
        ],
        # Описываем возможные ответы
        responses={
            200: PostSerializer(many=True),
            401: OpenApiResponse(description="Требуется аутентификация"),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return queryset of posts with related author and comments prefetched.
        """
        return Post.objects.select_related('author').prefetch_related(
            'comments')

    def get_permissions(self):
        """
        Return appropriate permission classes based on the action.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]

    def perform_create(self, serializer):
        """
        Save the post with the author.

        Args:
            serializer (PostSerializer): The serializer instance.
        """
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'list':
            return ShortPostSerializer
        return PostSerializer

    @action(detail=True, methods=['post'], url_path='publish',
            url_name='publish',
            permission_classes=[IsAuthor])
    def publish(self, request, pk):
        """
        Publish a post.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the post.

        Returns:
            Response: The response object.
        """
        post = self.get_object()
        if post.published:
            return Response({'message': 'Post is already published'},
                            status=400)
        post.published = True
        post.save(update_fields=['published'])
        return Response({'message': 'Post published successfully'}, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for comments.

    This viewset provides endpoints for creating, listing, retrieving and
    updating comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['content', 'post__title', 'post__content']
    ordering_fields = ['created_at', 'post']

    def get_permissions(self):
        """
        Set permissions based on the action being performed.

        Returns:
            list: List of permission classes.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthor()]

    def perform_create(self, serializer):
        """
        Save the comment with the author.

        Args:
            serializer (CommentSerializer): The serializer instance.
        """
        author, _ = Author.objects.get_or_create(user=self.request.user)
        serializer.save(author=author)
