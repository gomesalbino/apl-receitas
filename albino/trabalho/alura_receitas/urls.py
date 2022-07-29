
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from apps.usuarios.views import handler404


urlpatterns = [
    path('', include('receitas.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.usuarios.views.handler404"



