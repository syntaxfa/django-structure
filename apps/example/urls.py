from django.urls import path, include

from apps.example.views.post import PostDetailView

urlpatterns = [
    path("posts", include(([
        path("detail/<int:post_id>/", PostDetailView.as_view(), name="detail")
    ]))),
]
