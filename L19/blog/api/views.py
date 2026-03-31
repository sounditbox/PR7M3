from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer


# CRUD - Create Read Update Delete
# Retrieve List Create Update Destroy

class CreatePostAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

