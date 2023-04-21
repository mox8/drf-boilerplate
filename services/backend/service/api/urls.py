from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from apps.admin.admins import admin_site

from .v1.urls import urlpatterns as v1_urls
from .health_check import urlpatterns as health_check_urls


urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/', include([
        path('v1/', include(v1_urls)),
        path('health_check/', include(health_check_urls)),
    ]))
] + (
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
