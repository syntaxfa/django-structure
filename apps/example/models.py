from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.example.config import PostConfig


class Post(BaseModel):
    title = models.CharField(max_length=PostConfig.title_max_length, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"id: {self.id} title: {self.title}"
