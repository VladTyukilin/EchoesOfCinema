from django.contrib.sitemaps import Sitemap
from movie.models import Movie

class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Movie.published.all()

    def lastmod(self, obj):
        return obj.time_update