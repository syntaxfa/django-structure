from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework import serializers


class PageNumberPagination(_PageNumberPagination):
    max_page_size = 100
    page_size = 35
    page_size_query_param = 'page_size'


class ListResponse(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(default="next page link")
    previous = serializers.CharField(default="previous page link")
