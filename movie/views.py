from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from movie.models import Movie, PublishedModel, TagPost
from movie.forms import AddMovieForm, UploadImageForm
from movie.utils import DataMixin
from django.core.paginator import Paginator
from echoesofcinema import settings
from requests.adapters import HTTPAdapter
import requests
from .menu import MENU_ITEMS


menu = MENU_ITEMS


class MovieHome(LoginRequiredMixin, DataMixin, ListView):
    model = Movie
    template_name = 'movie/index.html'
    title_page = 'Главная страница'
    paginate_by = 3
    context_object_name = 'posts'


def about(request):
    about = ('Echoes of Cinema — приложение для управления своей киноколлекцией,'+' '
             'которое призвано отслеживать просмотренные фильмы и сериалы, а также планировать следующие просмотры.'+ ' '
             'Добавляйте фильмы, загружайте постеры и оставляйте личные заметки.')

    data = {'title': 'О сайте', 'mainmenu': menu, 'content': about}
    return render(request,'movie/about.html', context=data)


@login_required
def success(request):
    data = {'title': 'Успешно добавлено!', 'mainmenu': menu}
    return render(request,'movie/success.html', context=data)

def contact(request):
    pochta = 'Почта для связи: zelenogloid@mail.ru'

    context = {'title': pochta, 'mainmenu': menu}
    return render(request, 'movie/contact.html', context=context)

class Show_post(DetailView):
    model = Movie
    template_name = 'movie/post.html'
    context_object_name = 'movie'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UploadImageForm(instance=self.object)
        context['menu'] = menu
        context['title'] = 'Отображение добавленного фильма'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = UploadImageForm(request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            form.save()
            return redirect('post', slug=self.object.slug)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def login(request):
    return HttpResponse("Авторизация")


class AddMovieView(LoginRequiredMixin, DataMixin, CreateView):
    model = Movie
    form_class = AddMovieForm
    template_name = 'movie/add_movie.html'
    success_url = reverse_lazy('success')
    title_page = 'Добавление фильма/сериала'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePosterView(UpdateView):
    model = Movie
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Загрузка постера',
    }
