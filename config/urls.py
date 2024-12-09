""" URL configuration """
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
