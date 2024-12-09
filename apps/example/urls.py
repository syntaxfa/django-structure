from django.urls import path, include

from apps.example.views.post import PostListView, PostDetailView

urlpatterns = [
    path("posts", include(([
        path("", PostListView.as_view(), name="list"),
        path("detail/<int:post_id>/", PostDetailView.as_view(), name="detail")
    ]))),
]
