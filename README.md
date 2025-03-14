# Game Library 🎮

**Демонстрационный проект (портфолио)**

## Описание проекта

Game Library — это демонстрационная веб-платформа, предназначенная для создания и управления персональной библиотекой видеоигр. Проект позволяет пользователям просматривать каталог игр, добавлять понравившиеся игры в избранное или корзину, а также публиковать собственные игры. Данный проект служит примером реализации функционала с использованием современных технологий.

## Возможности

- **Просмотр игр:** Каталог видеоигр с подробными описаниями.
- **Регистрация и вход:** Возможность регистрации, авторизации (включая вход через сторонние сервисы) и восстановления пароля.
- **Управление играми:** Добавление, редактирование и удаление игр пользователями.
- **Корзина и избранное:** Сохранение игр в корзине для покупки или в списке избранного.
- **Комментарии:** Оставление отзывов и комментариев к играм.
- **Сообщения:** Отправка сообщений администраторам проекта.

## Используемые технологии

- **Backend:** Django, Django REST Framework, PostgreSQL
- **Frontend:** HTML, Tailwind CSS, JavaScript, jQuery
- **Деплой:** Docker, Nginx

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

## Примеры страниц сайта

1. Домашняя страница:
   
![image](https://github.com/user-attachments/assets/2e9282ed-9312-41d4-b584-94b17b9f3178)


3. Страница "О нас":
   
![image](https://github.com/user-attachments/assets/1af82378-1d27-4403-a97d-eb9a79976b53)

4. Страница "Игры":
   
![image](https://github.com/user-attachments/assets/46762943-859d-45ac-9a36-83ae36d224e8)

3.1 Информация об игре:

![image](https://github.com/user-attachments/assets/c0802930-1a18-4ee1-9324-b134222dbe2c)

3.2 Информация об игре (если игра твоя):

![image](https://github.com/user-attachments/assets/cd1c13c1-ca4e-462f-96c2-27d7fa654c48)

3.3 Изменение данных игры:

![image](https://github.com/user-attachments/assets/a418835c-c25a-4b4b-b478-f70b62037b34)

4. Страница "Контакты":
   
![image](https://github.com/user-attachments/assets/902ceea5-ae49-4df7-99a3-b934f242879d)

6. Регистрация
   
5.1 Вход:

![image](https://github.com/user-attachments/assets/71a050ff-d9ba-4958-9318-c93348f396c0)


5.2 Регистрация:

![image](https://github.com/user-attachments/assets/5621f701-6dc1-4437-8031-1654b0fcbd47)


6. Профиль:
   
![image](https://github.com/user-attachments/assets/7d9c0429-9cdf-480f-bc3e-b55f6c30c211)













