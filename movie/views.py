from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import CreateView
from movie.models import Movie, PublishedModel, TagPost
from movie.forms import AddMovieForm
from movie.utils import DataMixin
from django.core.mail import send_mail
from echoesofcinema.settings import DEFAULT_FROM_EMAIL
from django.core.paginator import Paginator


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить пост", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]

# data_db = [
#     {'id': 1, 'title': 'Властелин колец', 'content': '''Описание фильма: "Властелин колец" <p>Сказания о Средиземье — это хроника Великой войны за Кольцо, длившейся не одну тысячу лет. Тот, кто владел Кольцом, получал неограниченную власть, но был обязан служить злу. </p>''', 'is_published': True},
#     {'id': 2, 'title': 'Аркейн', 'content': '''Описание сериала: "Аркейн" <p>История разворачивается в утопическом краю Пилтовер и жестоком подземном городе Заун и рассказывает о становлении двух легендарных чемпионов Лиги и о той силе, что разведёт их по разные стороны баррикад.</p>''', 'is_published': False},
#     {'id': 3, 'title': 'Клиника', 'content': '''Описание сериала: "Клиника" <p>Отучившись четыре года в медицинской школе, Джон Дориан приходит работать интерном в клинику. Вместе с ним здесь же будет применять полученные знания и его лучший друг со времен колледжа Крис Терк. Не имеющие опыта практической работы, молодые специалисты сразу же погружаются в хаотический мир жизни больницы</p>''', 'is_published': True},
# ]

cats_db = [
    {'id': 1, 'name': 'Отложенные к просмотру'},
    {'id': 2, 'name': 'Не просмотрено'},
    {'id': 3, 'name': 'Уже просмотрено'},
]

class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# Create your views here.
def index(request):
    posts_list = Movie.published.all()
    paginator = Paginator(posts_list, 5)  # 5 постов на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'page_obj': page_obj,
    }
    return render(request, 'movie/index.html', context=data)

@login_required
def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request,'movie/about.html', context=data)

def show_post(request, post_slug):
    post = get_object_or_404(Movie, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'movie/post.html', context=data)

def show_category(request, cat_id):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Movie.published.filter(cat_id=category.pk).select_related("cat")

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'movie/index.html', context=data)



def viewed(request, viewed_id):
    return HttpResponse(f"<h1>Просмотренное</h1><p >id:{viewed_id}</p>")

def viewed_by_slug(request, viewed_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Просмотренное</h1><p >slug:{viewed_slug}</p>")

def unviewed(request, unviewed_id):
    return HttpResponse(f"<h1>Непросмотренное</h1><p >id:{unviewed_id}</p>")

def unviewed_by_slug(request, unviewed_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1>Непросмотренное</h1><p >slug:{unviewed_slug}</p>")

def archive(request, year):
    if year > 2025:
        url_redirect = reverse('viewed', args=('comedy', ))
        return redirect(url_redirect)
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

#LoginRequiredMixin, DataMixin, CreateView

# def addpage(LoginRequiredMixin, DataMixin, CreateView, PermissionRequiredMixin):
#     if request.method == 'POST':
#         form = AddMovieForm(request.POST)
#         if form.is_valid():
#             movie = form.save(commit=False)
#             movie.user = request.user
#             movie.save()
#             return redirect('home')
#     else:
#         form = AddMovieForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление фильма/сериала',
#         'form': form
#     }
#     return render(request, 'movie/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Movie.Status.PUBLISHED).select_related("cat")

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'cat_selected': None,
        'posts': posts,
    }

    return render(request, 'movie/index.html', context=data)


class AddMovieView(LoginRequiredMixin, DataMixin, CreateView):
    model = Movie
    form_class = AddMovieForm
    template_name = 'movie/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление фильма/сериала'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# def test_email(request):
#     try:
#         # Добавим подробный вывод для отладки
#         import smtplib
#         from django.core.mail import get_connection
#
#         connection = get_connection()
#         connection.open()
#         connection.close()
#
#         send_mail(
#             'Тестовое письмо от Django',
#             'Это тестовое письмо для проверки SMTP настроек',
#             'no-reply@echoesofcinema.com',
#             ['tyukilin-vlad@yandex.ru'],
#             fail_silently=False,
#         )
#         return HttpResponse("Письмо отправлено успешно!")
#     except Exception as e:
#         import traceback
#         return HttpResponse(f"Ошибка при отправке: {str(e)}<br>Трассировка: {traceback.format_exc()}")