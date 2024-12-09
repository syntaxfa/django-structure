from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView

from apps.api.response import base_response
from apps.example.codes import response_with_error
from apps.example.serializers.post import PostSerializer
from apps.example.services.post import get_post_service

SCHEMA_TAGS = ("Example/Posts",)
service = get_post_service()


class PostDetailView(APIView):
    serializer_class = PostSerializer

    @extend_schema(tags=SCHEMA_TAGS)
    def get(self, _, post_id: int):
        try:
            return base_response(status_code=status.HTTP_200_OK, result=self.serializer_class(
                instance=service.get_post(post_id=post_id)).data)
        except Exception as err:
            return response_with_error(err)
