from django.urls import path, include

from apps.authentication.views import TokenBanView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("token/", include(([
        path("verify/", TokenVerifyView.as_view(), name="token-verify"),
        path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
        path("logout/", TokenBanView.as_view(), name="token-ban"),
    ]
    ))),
]
