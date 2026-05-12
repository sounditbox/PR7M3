from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PostPagination(PageNumberPagination):
    ordering = '-created_at'
    page_size = 20
    max_page_size = 100
    page_query_param = 'p'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'data': data,
        })


class CommentPagination(PageNumberPagination):
    ordering = '-created_at'
    page_size = 5
    max_page_size = 20

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['data'] = data
        del response.data['results']
        return response