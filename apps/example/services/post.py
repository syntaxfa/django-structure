from dataclasses import dataclass
from functools import cache

from django.core.cache import cache as django_cache

from apps.example import codes
from apps.example.models import Post
from apps.common.raising import raise_and_log
from constants import example
from pkg.rich_error.error import RichError


@dataclass
class Config:
    post_cache_exp_in_seconds: int = 900  # 15 minutes
    post_cache_key: str = "posts"


class PostService:
    Op = "example.services.PostService."

    def __init__(self, config: Config):
        self.config = config

    def _get_post_by_id_or_raise(self, post_id: int):
        op = self.Op + "_get_post_by_id_or_raise"
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist as err:
            raise (RichError(op).set_error(err).set_msg(f"post with id {post_id} not found").
                   set_code(codes.POST_NOT_FOUND))

    def _get_post_key(self, post_id: int):
        return f"{self.config.post_cache_key}:{post_id}"

    def get_post(self, post_id: int):
        op = self.Op + "get_post"
        meta = {"post_id": post_id}

        try:
            key = self._get_post_key(post_id=post_id)
            post = django_cache.get(key=key)
            if post:
                return post

            post = self._get_post_by_id_or_raise(post_id=post_id)
            django_cache.set(key=key, value=post, timeout=self.config.post_cache_exp_in_seconds)
            return post
        except Exception as err:
            raise_and_log(example.APP_NAME, op, err, example.POST_SERVICE_GET_POST, example.POST_SERVICE_GET_POST, meta)


@cache
def get_post_service():
    return PostService(
        config=Config()
    )
