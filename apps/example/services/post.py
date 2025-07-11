from functools import cache

from django.core.cache import cache as django_cache

from apps.example import codes
from apps.example.config import PostServiceConfig
from apps.example.models import Post
from apps.example import constants
from apps.common.raising import err_log
from pkg.rich_error.error import RichError


class PostService:
    Op = "example.services.post.PostService."

    def __init__(self, cfg: PostServiceConfig):
        self.cfg = cfg

    def _get_post_by_id_or_raise(self, post_id: int):
        op = self.Op + "_get_post_by_id_or_raise"
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist as err:
            raise (RichError(op).set_error(err).set_msg(f"post with id {post_id} not found").
                   set_code(codes.POST_NOT_FOUND))

    def _get_post_key(self, post_id: int):
        return f"{self.cfg.post_cache_key}:{post_id}"

    def get_post(self, post_id: int):
        meta = {"post_id": post_id}

        try:
            key = self._get_post_key(post_id=post_id)
            post = django_cache.get(key=key)
            if post:
                return post

            post = self._get_post_by_id_or_raise(post_id=post_id)
            django_cache.set(key=key, value=post, timeout=self.cfg.post_cache_exp_in_seconds)
            return post
        except Exception as err:
            err_log(constants.APP_NAME, err, constants.POST_SERVICE, constants.GET_POST, meta)
            raise err


@cache
def get_post_service():
    return PostService(
        cfg=PostServiceConfig(),
    )
