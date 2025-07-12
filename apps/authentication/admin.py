from django.contrib import admin

from .models import UserAuth


@admin.register(UserAuth)
class UserAuthAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "created_at", "updated_at")
    search_fields = ("user_id",)
