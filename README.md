# CookBook - «Продуктовый помощник»
Дипломный проект разработанный в рамках учебного курса от Яндекс.Практикум.

Цель работы - закрепить опыт, полученные в процессе обучения.

[![Testing](https://github.com/wurikavich/cookbook/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/wurikavich/cookbook/actions/workflows/main.yml)

## Описание
Проект **Cook Book** - Продуктовый помощник, онлайн-сервис и API для него.
На этом сервисе пользователи публикуют свои рецепты, добавляют понравившиеся
рецепты в избранное и подписываться на публикации любимых авторов, 
а перед походом в магазин могут скачивать сводный список продуктов в формате pdf,
необходимых для приготовления одного или нескольких выбранных блюд, добавленных в список покупок.

## Функционал:
### Пользователи:
- Каждый пользователь имеет свою роль:
   - Анонимный пользователь
   - Аутентифицированный пользователь
   - Администратор
- Получение данных своей учетной записи
- Получение данных пользователя по id
- Получение списка всех пользователей
- Регистрация пользователя
- Изменение пароля своей учетной записи
- Получение токена авторизации
- Удаление токена авторизации

### Подписки:
- Получение списка пользователей, на которых подписан пользователь
- Подписаться на пользователя
- Отписаться от пользователя

### Теги:
- Получение списка всех тегов
- Получение данных тега по id

### Ингредиенты:
- Получение списка всех индентов
- Получение данных ингредиента по id

### Рецепты:
- Получить список всех опубликованных рецептов
- Получение информации о рецепте по id
- Добавление рецепта
- Частичное обновление информации о рецепте
- Удаление рецепта

### Избранные рецепты:
- Добавить рецепт в избранное
- Удалить рецепт из избранного

### Список покупок:
- Скачать pdf-файл со списком необходимых ингредиентов
- Добавить рецепт в список покупок
- Удалить рецепт из списка покупок

## Настройка и запуск:
Для развертывания проекта необходимо установить и запустить [Docker](https://www.docker.com/products/docker-desktop/).

1. Клонируем репозиторий на локальную машину:
   ```bash
   git git@github.com:wurikavich/cookbook.git
   ```
   
2. В директории infra создаём файл .env, со следующими переменными:
   - Создаём файл:
      ```bash
      cd cookbook\infra  # Переместились в директорию infra
      nano .env  # Создали и открыли файл .env
      ```
   - Прописываем переменное окружения в нём. [Сгенерируйте секретный ключ.](https://djecrety.ir/):
      ```bash
      POSTGRES_ENGINE=django.db.backends.postgresql  # указываем, что работаем с postgresql
      POSTGRES_DB=postgres  # имя базы данных (можете изменить)
      POSTGRES_USER=postgres  # логин для подключения к базе данных (можете изменить)
      POSTGRES_PASSWORD=postgres  # пароль для подключения к БД (можете изменить)
      POSTGRES_HOST=db  # название сервиса-контейнера
      POSTGRES_PORT=5432  # порт для подключения к БД
      SECRET_KEY=  # секретный ключ Django (вставьте сгенерированный ключ)
      DEBUG=False
      ALLOWED_HOSTS=  # при развертывании локально необходимо указать - localhost 127.0.0.1 *
      ```
   - Сохраняем изменения в файле.

3. Запуск контейнеров Docker:
   - Из директории infra необходимо выполнить команду:
      ```bash
      docker-compose up -d --build
      ```
   - Ждем выполнение команды, при успешном выполнении, в терминале должны быть следующии строчки:
      ```bash
      Creating infra_db_1 ... done
      Creating infra_backend_1 ... done
      Creating infra_frontend_1 ... done
      Creating infra_nginx_1   ... done
      ```

4. Запуск django проекта. Из директории infra, выполняем команды:
   - Создаём и применяем миграции:
      ```bash
      docker-compose exec backend python manage.py makemigrations
      docker-compose exec backend python manage.py migrate
      ```
   - Подключаем статику:
      ```bash
      docker-compose exec backend python manage.py collectstatic --no-input
      ```
   - Загружаем подготовленные данный в базу данных проекта:
      ```bash
      docker-compose exec backend python manage.py loaddata data/fixtures.json
      ```     
   - Создаём супер пользователя django:
      ```bash
      docker-compose exec backend python manage.py createsuperuser
      ```

Приведенные выше инструкции по установке и запуску проекта имеют только 
демонстрационную цель и могут быть использованы только на [localhost]((http://localhost/recipes/)). 

Документация, запустите сервер и перейдите по ссылке: [http://localhost//api/docs/](http://localhost/api/docs/).

Панель аднимистратора: [http://localhost/admin/](http://localhost/admin/). 

## Примеры запросов на эндпоинты
### Регистрация нового пользователя:
#### Запрос
```bash
POST - 'http://localhost/api/users/'
{
    "username": "user_username.",
    "email": "user@mail.ru",
    "password": "user_password.",
    "first_name": "user_first_name",
    "last_name":"user_last_name"
}
```

#### Ответ
```bash
{
    "id": 2,
    "username": "user_username.",
    "email": "user@mail.ru",
    "first_name": "user_first_name",
    "last_name": "user_last_name"
}
```

### Получение токена:
#### Запрос
```bash
POST - 'http://localhost/api/auth/token/login/'
{
    "password": "user_password.",
    "email": "user@mail.ru"
}
```

#### Ответ
```bash
{
    "auth_token": "token_value"
}
```

### Получение данных своей учетной записи:
#### Запрос
```bash
GET - 'http://localhost/api/users/me/'
header 'Authorization: Token "token_value"'
```

#### Ответ
```bash
{
    "id": 2,
    "username": "user_username.",
    "email": "user@mail.ru",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "is_subscribed": false
}
```

## Стек технологий
### Backend:
- Python 3.10
- Django 3.2.16
- Django REST Framework 3.14.0

### Инфраструктура для запуска:
- Docker-compose
- Nginx
- Gunicorn
- PostgreSQL

### Запуск на сервере  

Реализовано развертывание на Виртуальной Машине, сервера [Яндекс.Облако](https://cloud.yandex.ru/)  

с помощью GitHub Actions в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn.

## Разработчик
[Александр Гетманов](https://github.com/wurikavich)