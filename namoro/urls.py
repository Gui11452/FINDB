from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('perfil/', include('perfil.urls')),
    path('eventos/', include('eventos.urls')),
    path('payment/', include('payment.urls')),
    path('comunication/', include('comunication.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'produto.views.not_found'
