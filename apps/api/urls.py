from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


doc_urls = [
    path("", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(), name="redoc"),
]

v1 = [
    path("schema/", include(doc_urls), name="schema"),
    path("examples/", include("apps.example.urls"), name="example"),
]

urlpatterns = [
    path("v1/", include(v1)),
]
