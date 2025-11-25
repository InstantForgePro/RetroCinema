from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from catalog import views as catalog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalog_views.home, name='home'),
    path('movie/<int:pk>/', catalog_views.movie_detail, name='movie_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
