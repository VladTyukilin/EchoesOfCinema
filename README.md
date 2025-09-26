# Echoes of Cinema


## Скриншоты

![Главная страница Echoes of Cinema](screenshots/homepage.png)
![Страница добавления фильма](screenshots/post.png)

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
1. Убедитесь, что [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/install/) установлены.

2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/VladTyukilin/EchoesOfCinema.git
   ```
   
3. Перейдите в директорию проекта:
   ```bash
   cd EchoesOfCinema
   ```
   
4. Соберите и запустите контейнер:
   ```bash
   docker-compose up --build
   ```
   
5. Откройте в браузере:
   http://localhost:8000

💡 При первом запуске Docker автоматически применит миграции и запустит сервер

или

Вариант через `docker run` требует ручного применения миграций 

1. Соберите образ: `docker build -t echoesofcinema .`
2. Запустите контейнер: `docker run -p 8000:8000 echoesofcinema`
3. Перейдите в браузере по адресу: `http://localhost:8000`

## Настройка окружения
1. Создайте файл `.env` на основе шаблона:
   ```bash
   cp .env.example .env  # Linux/Mac
   copy .env.example .env  # Windows (cmd)
   ```

2. Сгенерируйте SECRET_KEY с помощью:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```   

3. Укажите `DEBUG=True`

## Структура проекта

echoesofcinema/                 # Основной Django-проект
├── echoesofcinema/             # Настройки проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── movie/                      # Приложение: управление фильмами и сериалами
│   ├── __init__.py
│   ├── models.py               # Модели данных
│   ├── views.py                # Представления
│   ├── urls.py                 # Маршруты
│   ├── forms.py                # Формы
│   ├── admin.py                # Админка
│   ├── apps.py
│   ├── utils.py
│   ├── menu.py
│   ├── templatetags/           # Кастомные шаблонные теги
│   │   └── movie_tags.py
│   ├── templates/movie/        # HTML-шаблоны
│   │   ├── index.html
│   │   ├── post.html
│   │   ├── add_movie.html
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── list_categories.html
│   │   ├── list_tags.html
│   │   └── success.html
│   ├── static/movie/           # Статические файлы (CSS, JS, изображения)
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── fixtures/               # Фикстуры для тестов
│       ├── movie_movie.json
│       ├── movie_category.json
│       ├── auth_user.json
│       └── ...
├── users/                      # Приложение: регистрация и аутентификация
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/              # Шаблоны пользовательских страниц
├── media/                      # Загруженные файлы (постеры)
│   └── posters/
├── manage.py
├── requirements.txt            # Зависимости Python
├── Dockerfile                  # Конфигурация Docker-образа
├── docker-compose.yml          # Запуск через Docker Compose
├── .env.example                # Пример файла окружения
├── .gitignore
├── .dockerignore
└── README.md


## Статические файлы
Для работы со статическими файлами:
1. Убедитесь, что STATIC_ROOT настроен в settings.py
2. Соберите статику: `python manage.py collectstatic`

## Тестирование
```bash
python manage.py test movie
```