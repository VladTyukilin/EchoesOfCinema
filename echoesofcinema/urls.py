from django.contrib import admin
from django.urls import path, include
from movie import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import urls
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

