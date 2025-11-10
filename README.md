# Курсовая работа #5 HabitTracker

## Многофункциональный трекер привычек с Django REST Framework, Celery, JWT и интеграцией Telegram

## Особенности
- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker, Docker Compose
- Nginx
- CICD
- GitHub Actions

## Основные приложения

- **users** — регистрация/логин с JWT, работа профиля, Telegram ID, права доступа
- **habits** — CRUD привычек, периодичность, напоминания, интеграция с celery
- **Celery** — фоновая отправка уведомлений (например, Telegram)
- **JWT** — авторизация через токены
- **Phonenumber** — поддержка телефонов в профиле

# Установка и запуск

## 1. Клонирование
~~~
git clone https://github.com/Konstantin-Voronin-23/DRF_KR.git
cd DRF_KR
~~~

## 2. Создание файла переменных окружения:

* Скопируйте .env.sample в .env и укажите свои значения:
~~~
cp .env.sample .env
~~~

## 3. Сборка и запуск контейнеров:
~~~
docker compose up -d --build
~~~

## 4. Запуск и миграция базы данных:
~~~
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
~~~

## 5. Создание суперюзера | админка:
~~~
docker compose exec web python manage.py createsuperuser
~~~

## 6. Доступ к API и админке:

Админка: http://localhost:8000/admin/

API: http://localhost:8000/habits/

# Деплой на сервер

## 1. Подключение к серверу:
~~~
ssh <USER>@<SERVER_IP>
cd /var/server/DRF_KR
~~~

## 2.  Получение последних изменений:
~~~
git pull origin main
~~~

## 3. Обновление контейнеров:
~~~
docker compose down
docker compose up -d --build
~~~

## 4. Миграции и статические файлы:
~~~
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
~~~


# Авторизация в API

* Для большинства запросов нужен JWT-токен.

* Получение токена:
~~~
POST /api/token/
Content-Type: application/json

{
  "email": "<email>",
  "password": "<password>"
}
~~~

* Использование токена во всех запросах:
~~~
Authorization: Bearer <ваш_access_token>
~~~

## API Endpoints

- `POST /users/register/` — регистрация нового пользователя
- `POST /users/login/` — аутентификация, получение JWT
- `POST /users/token/refresh/` — обновление JWT
- `GET/PATCH /users/user/` — просмотр и изменение профиля
- `POST /users/tg-profile/` — создание Telegram профиля
- `GET /habits/` — список привычек (требует авторизации)
- `POST /habits/` — создать привычку
- `DELETE /users/deactivate/` — деактивация пользователя

# CI/CD (GitHub Actions)
Процесс полностью автоматизирован:

* Запуск при пуше в ветки main, feature/dc_deploy_cicd, develop
* Проверка и сборка:
  1. Линтинг (flake8)
  2. Запуск тестов через Django manage.py test
  3. Сборка docker-образов

* Автоматический деплой:
  * По SSH, с помощью секретного ключа GitHub Actions
  * Остановка старых контейнеров и запуск новых с актуальным кодом

Необходимые Secrets в GitHub:
* SECRET_KEY — секретный ключ Django
* SERVER_HOST — IP-адрес сервера
* SERVER_USER — имя пользователя на сервере
* SERVER_SSH_KEY — приватный SSH-ключ для доступа
* SERVER_PORT - порт сервера
* TELEGRAM_BOT_TOKEN - токен тг бота

# Инструкция по настройке сервера для CI/CD
1. Генерация SSH-ключа для GitHub Actions:
~~~
ssh-keygen -t rsa -b 4096 -C "github-actions-deploy"
~~~

2. Добавьте публичный ключ в файл ~/.ssh/authorized_keys на сервере.
3. Загрузите приватный ключ в секцию Secrets GitHub Actions как SERVER_SSH_KEY.
4. В workflow .github/workflows/ci-cd.yml обязательно проверьте путь к проекту для шага деплоя

## Дополнительно
* Статичный IP адрес сервера 89.169.176.175
* Swagger API: http://89.169.176.175:8000/swagger/
* Пример .env (настройка для локального теста):
~~~
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=habittracker_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=db
DB_PORT=5432
...
~~~ 

# Тесты
Запускаются автоматом через GitHub Actions и вручную:
~~~
docker compose exec web python manage.py test
~~~

# Полезные команды для контейнеров
* Стоп: docker compose down
* Запуск: docker compose up -d --build
* Логи: docker compose logs -f web
* Посмотреть контейнеры: docker compose ps

# Покрытие 87%

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE)
