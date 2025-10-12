from django.contrib import admin, messages
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content']
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('title', 'time_create', 'brief_info')
    list_display_links = ('title', )
    ordering = ['time_create', 'title']
    list_per_page = 5
    search_fields = ['title__startswith']


    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, movie: Movie):
        return f"Описание {len(movie.content)} символов."