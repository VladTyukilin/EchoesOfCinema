from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

a = get_user_model()


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

## Здесь используется стандартное имя параметра username, чтобы наш новый бэкенд согласованно работал с фреймворком Django.
# Но мы подразумеваем, что сюда будет передаваться E-mail, по которому, затем, выделяется запись из таблицы user.
# Если запись найдена и пароль совпадает, то аутентификация прошла успешно и возвращается объект пользователя.
# Иначе возвращаем None, а также в том случае, если запись не была найдена или было получено несколько записей с указанным E-mail

# То есть, у нас будут работать оба бэкенда: и по логину и по E-mail.
# Эти классы просматриваются по порядку в списке и срабатывает первый вернувший объект пользователя, остальные пропускаются.
# В результате, пользователи могут авторизоваться и по логину и по E-mail.