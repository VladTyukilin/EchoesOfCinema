from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.sitemaps.views import sitemap

# sitemaps = {
#     'posts': PostSitemap,
# }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('users/', include('users.urls', namespace='users')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

