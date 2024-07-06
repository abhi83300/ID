from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import index, scan_qr, generate_qr

urlpatterns = [
    path('', index, name='index'),
    path('scan_qr/', scan_qr, name='scan_qr'),
    path('generate_qr/', generate_qr, name='generate_qr'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)