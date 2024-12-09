from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework import serializers


class PageNumberPagination(_PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_number'
    max_page_size = 1000

    def __init__(self, page_size: int = 12, page_size_query_params: str = "page_size", max_page_size: int = 25):
        self.page_size = page_size
        self.page_query_param = page_size_query_params
        self.max_page_size = max_page_size


class ListResponse(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(default="next page link")
    previous = serializers.CharField(default="previous page link")
