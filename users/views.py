from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.shortcuts import redirect
from .forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


# class CustomLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('home')  # или settings.LOGOUT_REDIRECT_URL


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


# класс представления для работы с этой формой ProfileUserForm (форма для шаблона profile.html)
class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user

# свой класс представления для отображения собственной формы смены пароля
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
