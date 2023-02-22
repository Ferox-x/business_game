from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.authenticate.urls")),
    path("", include("apps.users.urls")),
    path("", include("apps.business_game.urls")),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
