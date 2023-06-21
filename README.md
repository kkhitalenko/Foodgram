![foodgram_workflow](https://github.com/kkhitalenko/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodgram
Foodgram - продуктовый помощник, онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Необходимые технологии: Docker, Docker-Compose

## Как запустить проект на удалённом сервере:

- Клонировать репозиторий и перейти в него в командной строке

```
git clone git@github.com:kkhitalenko/foodgram-project-react/
```

```
cd foodgram-project-react/infra/
```
- В файле nginx.conf указать свой IP-адрес или доменное имя в строке server_name
- Скопировать nginx.conf и docker-compose.yml на сервер с помощию sftp:
```
$ sftp {user}@{host}:{remote-path} <<< $'put {local-path}'
```
- Создать .env файл и заполнить его по аналогии с файлом .env.example
- Для того, чтобы workflow корректно отработал, необходимо добавить в GitHub Actions следующие переменные в secrets. Для этого нужно перейти в настройки репозитория Settings, выбрать на панели слева Secrets, нажать New secret и последовательно добавлять каждую переменную
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных postgres, как в файле .env>
POSTGRES_USER=<логин для подключения к базе данных, как в файле .env>
POSTGRES_PASSWORD=<пароль для подключения к БД, как в файле .env>
DB_HOST=db
DB_PORT=5432
DOCKER_PASSWORD=<ваш пароль от DockerHub>
DOCKER_USERNAME=<ваше имя пользователя на DockerHub>
USER=<имя пользователя для подключения к серверу>
HOST=<IP-адрес вашего сервера>
PASSPHRASE=<если при создании ssh-ключа вы использовали фразу-пароль, укажите её здесь>
SSH_KEY=<приватный ключ с компьютера, имеющего доступ к боевому серверу>
```
Последующая работа будет проходить на сервере, поэтому необходимо 
- подключиться к серверу с помощью ssh:
```
$ ssh <имя пользователя для подключения к серверу>@<IP-адрес вашего сервера>
```
- запустить docker-compose
```
sudo docker-compose up -d --build
```
- при первом запуске необходимо будет выполнить следующие команды:
  ```
  sudo docker-compose exec backend python manage.py makemigrations
  sudo docker-compose exec backend python manage.py migrate users
  sudo docker-compose exec backend python manage.py migrate
  sudo docker-compose exec backend python manage.py collectstatic --noinput
  sudo docker-compose exec backend python manage.py createsuperuser
  sudo docker-compose exec backend python manage.py import_json
  ```
  
## Доступность проекта:
Документация и примеры запросов доступны по адресу http://84.252.139.113/api/docs/

Учетные данные для входа через администратора:
- логин: admin
- почта: admin@admin.ru 
- пароль: admin12345admin


## Используемые технологии:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

