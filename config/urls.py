from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("appointments/", include("appointments.urls")),
    path("accounts/", include("accounts.urls")),
    # API-эндпоинты на верхнем уровне для единообразия
    path("api/", include("accounts.api_urls")),  # отдельный модуль для API
]

# Добавляем статические и медиафайлы только один раз
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Для локальной разработки: поддержка старых путей к изображениям
    images_root = (settings.BASE_DIR.parent / "images").resolve()
    urlpatterns += static("/images/", document_root=images_root)
