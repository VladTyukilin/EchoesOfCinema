from django.urls import path, register_converter
from movie import views


urlpatterns = [
    path('', views.MovieHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('post/<slug:slug>/', views.Show_post.as_view(), name='post'),
    path('add_movie/', views.AddMovieView.as_view(), name='add_movie'),
    path('success/', views.success, name='success'),
]