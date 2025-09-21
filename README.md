# Echoes of Cinema

## Описание
Сайт для отслеживания просмотренных и запланированных к просмотру фильмов и сериалов.

## Функционал
- Регистрация, аутентификация и авторизация пользователей
- Восстановление пароля
- Добавление фильма/сериала
- Добавление постеров
- Пагинация страниц

## Технологии
- Python 3.11
- Django 5.2
- HTML/CSS (базовые знания)

## Запуск проекта
1. Создайте виртуальное окружение: `python -m venv .venv`
2. Активируйте: `source .venv/bin/activate` (Linux/Mac) или `.venv\Scripts\activate` (Windows)
3. Перейдите в директорию с проектом: `cd <Буква Диска>\Projects\<Имя проекта>\<Директория проекта>`
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте суперпользователя: `python manage.py createsuperuser`
6. Запустите миграции: `python manage.py migrate`
7. Запустите сервер: `python manage.py runserver`

## Запуск через Docker
1. Соберите образ: `docker build -t echoesofcinema .`
2. Запустите контейнер: `docker run -p 8000:8000 echoesofcinema`
3. Перейдите в браузере по адресу: `http://localhost:8000`

или

1. Убедьтесь, что Docker и Docker Compose установлены
2. Выполните:  
   docker-compose up --build

## Настройка окружения
1. Создайте файл `.env` на основе `.env.example` (если есть)
2. Укажите `SECRET_KEY` и `DEBUG=True`
3. Не забывайте добавлять `.env` в `.gitignore`

## Структура проекта
- `echoesofcinema/` - основной проект
- `movie/` - приложение для управления фильмами
  - `templates/` - шаблоны
  - `forms.py` - формы
  - `models.py` - модели данных
  - `tests.py` - тесты
  - `urls.py` - пути
  - `views.py` - представления
- `users/` - приложение для регистрации/аутентификации/авторизации
  - `templates/` - шаблоны
  - `forms.py` - формы
  - `urls.py` - пути
  - `views.py` - представления

## Статические файлы
Для работы со статическими файлами:
1. Убедитесь, что STATIC_ROOT настроен в settings.py
2. Соберите статику: `python manage.py collectstatic`

## Тестирование
python manage.py test movie