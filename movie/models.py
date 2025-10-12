from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название фильма')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank=True, null=True)
    content = models.TextField(blank=True, verbose_name='Короткое описание')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) ## привязка к конкретному пользователю.
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name="Постер")

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # Используем unidecode для транслитерации кириллицы
            base_slug = slugify(unidecode(self.title))
            slug = base_slug
            counter = 1
            while Movie.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Фильм/Сериал'
        verbose_name_plural = 'Фильмы/Сериалы'
        ordering = ['time_create']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})