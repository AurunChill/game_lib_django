# Game Library 🎮

**Портфолио / не воспринимать как настоящий проект!**

Добро пожаловать на [gamelib-portfolio.ru](http://gamelib-portfolio.ru) - вашу персональную библиотеку видеоигр! Здесь каждый найдет что-то для себя, от увлекательных приключений до сложных головоломок.

## 📚 Описание Сайта

Присоединяйтесь к нашей обширной библиотеке видеоигр. Окунитесь в захватывающие миры, где каждый найдет что-то по душе. Не упустите шанс погрузиться в мир игровой фантазии уже сегодня!

### Возможности сайта:

- 🔍 **Просмотр игр**: Исследуйте доступные игры.
- 🛒 **Добавление в корзину**: Добавляйте понравившиеся игры в корзину или желаемое.
- 📝 **Регистрация и вход**: Регистрация через Google или по сессии, восстановление и смена пароля.
- 🎮 **Добавление игр**: Пользователи могут выкладывать свои игры, а также обновлять или удалять их.
- 💬 **Комментарии**: Комментируйте игры и отвечайте на комментарии других пользователей.
- 📨 **Сообщения**: Отправляйте сообщения нашей компании.

## 🛠️ Используемые Технологии

- **Backend**: Django, Django REST Framework, PostgreSQL
- **Frontend**: HTML, Tailwind CSS, JavaScript, jQuery
- **Deployment**: Docker, Nginx

## 🚀 Запуск и Установка

### Локальная Установка

1. **Клонируйте репозиторий.**

    ```bash
    git clone 
    cd 
    ```

2. **Создайте и активируйте виртуальную среду.**

    ```bash
    poetry install
    ```

3. **Примените миграции.**

    ```bash
    poetry run python manage.py migrate
    ```

4. **Создайте суперпользователя.**

    ```bash
    poetry run python manage.py createsuperuser
    ```

5. **Запустите сервер.**

    ```bash
    poetry run python manage.py runserver
    ```

### Деплой с использованием Docker

Необходима предварительная установка Docker.

1. **Установите PostgreSQL на сервер и настройте конфигурации.**

    - Пропишите доступные хосты и IP-адреса, с которых можно отправлять запросы к базе данных.
    - Установите пароль для пользователя.
    - Перезапустите PostgreSQL.

    ```bash
    sudo systemctl restart postgresql
    ```

2. **Дайте права на выполнение entrypoint.sh.**

    ```bash
    chmod +x entrypoint.sh
    ```

3. **Запустите Docker Compose.**

    ```bash
    docker-compose up --build
    ```

## 📄 .env файл

Не забудьте создать файл `.env` со следующим содержимым:

```env
# Django Secret Key
SECRET_KEY=

# Database Data
DB_ENGINE="django.db.backends.postgresql"
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=

CURRENT_DB="postgres"  # Используйте 'sqlite' для SQLite и 'postgres' для PostgreSQL
```

✨ Наслаждайтесь погружением в мир игр на [gamelib-portfolio.ru](http://gamelib-portfolio.ru)!
