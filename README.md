## Business Games

____

## 1. Как запустить проект:


1) Клонировать репозиторий и перейти в него в командной строке:

`git clone https://gitlab.com/edgiek/business-games.git`

## 2. Запуск Backend'а

1) Cоздать и активировать виртуальное окружение в корне проекта:

`python -m venv venv`

`source venv/Scripts/activate`

2) Переходим в директорию backend:

`cd backend/`

3) Установить зависимости:


`python -m pip install --upgrade pip`

Для windows:

`pip install -r requirements_windows.txt`

Для linux:

`pip install -r requirements_linux.txt`

4) Запустить PostgreSQL Server.

Создать базу данных с названием проекта business-games.

*Если вы хотите создать базу данных с другим названием
не забудьте изменить его в .env файле (см. пункт 6)

5) Запустить Redis Server.


6) Создать и заполнить .env файл в соответствии с .env_example:

.env_example уже настроен для локальной разработки.

При запуске проекта. Нужно изменить раздел
#postgres.

POSTGRES_USER=ваш postgres пользователь
POSTGRES_PASSWORD=пароль от пользователя

При запуске локально дополнительно нужно изменить.

DB_HOST=127.0.0.1

Если у вас запущен PostgreSql Server на не стандартном порте
нужно изменить следующую переменную.

DB_PORT=порт

Указать локацию редиса.

LOCATION=127.0.0.1:6379

7) Выполнить миграции:

`python manage.py makemigrations`

`python manage.py migrate`

8) Загрузить фикстуры:

`python manage.py loaddata fixtures/*.json`

9) Запустить сервер:

`python manage.py runserver`


## 3. Запуск Frontend'а.

1) Установить node.js (https://nodejs.org/en/download/).

2) Перейти в директорию frontend.

`cd frontend/`

3) Установить зависимости:

`npm install`

4) Запустить React development server:

`npm start`

## 4. Запуск с помощью docker-compose

1) Установить docker-compose или Docker Desktop.

2) Заполнить .env файл по подобию .env_example. Нужно изменить только перменные
pgadmin. Так же можете изменить логины и пароли для вашего удобства

3) Перейти в корневую папку проекта (на уровне с docker-compose.yml).

4) Использовать команду.

`docker-compose up -d --build`

5) Полезная информация:

Frontend: `localhost:3000`

Backend: `localhost:8000`

PgAdmin: `localhost:80`

PgBouncer: `localhost:5432`

Redis: `localhost:6379`

## 5. Pre-commit (обязательно)

1) Убедитесь, что при установке backend'а выполнился 3 пункт. И установилась
библиотека pre-commit

2) В корне проекта выполняем следующею команду:

`pre-commit install`

3) Чтобы проверить codestyle, можно выполнить следующею команду:

`pre-commit run --all-files`
