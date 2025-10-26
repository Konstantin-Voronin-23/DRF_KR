# Курсовая работа #5 HabitTracker

## Многофункциональный трекер привычек с Django REST Framework, Celery, JWT и интеграцией Telegram

## Особенности
- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL

## Основные приложения

- **users** — регистрация/логин с JWT, работа профиля, Telegram ID, права доступа
- **habits** — CRUD привычек, периодичность, напоминания, интеграция с celery
- **Celery** — фоновая отправка уведомлений (например, Telegram)
- **JWT** — авторизация через токены
- **Phonenumber** — поддержка телефонов в профиле

# Установка и запуск

### Для работы приложения необходимо установить интерпретатор *poetry*:

```pip install --user poetry```

### Так же клонируйте репозиторий:

```git clone git clone https://github.com/Konstantin-Voronin-23/DRF_KR.git```

### Для работы проекта воспользуйтесь командами для установок зависимостей:

```
poetry add --group lint flake8
poetry add --group lint mypy
poetry add --group lint black
poetry add --group lint isort

poetry add python-dotenv
pip install psycopg2
poetry add django
poetry add Pillow
poetry add ipython
poetry add redis
pip install djangorestframework
poetry add  django-filter
poetry add djangorestframework-simplejwt
poetry add celery
pip install django-celery-beat
poetry add eventlet
poetry add drf-spectacular
```
## Настройка окружения

```
SECRET_KEY=ваш-secret-key
DEBUG=True

NAME=habittracker_db
USER=логин бд
PASSWORD=пароль бд
PORT=5432
HOST=localhost

REDIS_URL=redis://127.0.0.1:6379

TELEGRAM_BOT_TOKEN=ваш-tg_token
```

## Настройка базы данных

```
python manage.py migrate
python manage.py createsuperuser

```

## Запуск сервера

```
python manage.py runserver

```

### Приложение будет доступно по адресу: http://127.0.0.1:8000

### 5. Запуск с Gunicorn + Eventlet (для async/telegram/celery)

~~~
gunicorn -k eventlet config.wsgi:application
~~~


- В `config/wsgi.py` первой строкой:
import eventlet; eventlet.monkey_patch()

---

## API Endpoints

- `POST /users/register/` — регистрация нового пользователя
- `POST /users/login/` — аутентификация, получение JWT
- `POST /users/token/refresh/` — обновление JWT
- `GET/PATCH /users/user/` — просмотр и изменение профиля
- `POST /users/tg-profile/` — создание Telegram профиля
- `GET /habits/` — список привычек (требует авторизации)
- `POST /habits/` — создать привычку
- `DELETE /users/deactivate/` — деактивация пользователя

## Тестирование

~~~
python manage.py test
~~~

~~~
coverage run manage.py test
coverage report -m
coverage html
~~~

## Примеры запроса

### Регистрация

~~~
POST /users/register/
Content-Type: application/json
{
"email": "user@mail.com",
"password": "strongpass123",
"password2": "strongpass123"
}
~~~


### Получение и обновление профиля

~~~
GET /users/user/ # JWT обязательно
PATCH /users/user/
{
"city": "Москва",
"time_zone": "Europe/Moscow"
}
~~~


---

## Celery/Telegram

- Для отправки уведомлений по привычке запускаются задачи celery
- Telegram‑бот интегрируется через chat_id и API

# Покрытие 87%

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE)
