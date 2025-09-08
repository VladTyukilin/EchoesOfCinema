from django.urls import path, register_converter
from movie import converters, views


register_converter(converters.FourDigitYearConverter, "year4")
# handler404 = page_not_found

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('viewed/<int:viewed_id>/', views.viewed, name='viewed_id'),
    path('viewed/<slug:viewed_slug>/', views.viewed_by_slug, name='viewed'),
    path('unviewed/<int:unviewed_id>/', views.unviewed, name='unviewed_id'),
    path('unviewed/<slug:unviewed_slug>/', views.unviewed_by_slug, name='unviewed'),
    path('archive/<year4:year>/', views.archive, name='archive'),
    # path('addpage/', views.addpage, name='add_page'),
    path('addpage/', views.AddMovieView.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    # path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    # path('test-email/', views.test_email, name='test_email'),

]