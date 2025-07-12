from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class UserAuth(BaseModel):
    user_id = models.PositiveBigIntegerField(verbose_name=_("user id"), db_index=True, unique=True)
    access_uuid = models.UUIDField(verbose_name=_("access uuid"), unique=True, db_index=True)
    refresh_uuid = models.UUIDField(verbose_name=_("refresh uuid"), unique=True, db_index=True)

    class Meta:
        verbose_name = _("User Auth")
        verbose_name_plural = _("User Auths")
        ordering = ("-id",)

    def __str__(self):
        return f"id: {self.pk} user id: {self.user_id}"
