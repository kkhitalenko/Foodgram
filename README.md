![foodgram_workflow](https://github.com/kkhitalenko/Foodgram/actions/workflows/main.yml/badge.svg)

# Foodgram
Foodgram - продуктовый помощник, онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд

<details>
   <summary>Исходные данные</summary> 
  
- фронтенд на React;
- техническое описание проекта;
- Redoc спецификация API;
- список ингредиентов в формате JSON для загрузки в базу Postgres

</details>

<details>
   <summary>Что было сделано</summary> 
  
- создан Django-проект;
- создан API-сервис на базе проекта;
- настроено взаимодействие с фронтендом, написанным на React;
- созданы образы и запушены на DockerHub;
- созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;
- настроен CI/CD
</details>



<details>
   <summary>Запуск проекта на удалённом сервере</summary> 

Необходимые технологии: Docker, Docker-Compose

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:kkhitalenko/Foodgram/
```

```
cd Foodgram/infra/
```
- В файле nginx.conf указать свой IP-адрес или доменное имя в строке server_name
- Скопировать nginx.conf и docker-compose.yml на сервер с помощию sftp:
```
$ sftp {user}@{host}:{remote-path} <<< $'put {local-path}'
```
- Создать .env файл и заполнить его по аналогии с файлом .env.example
- Для того, чтобы workflow корректно отработал, необходимо добавить в GitHub Actions следующие переменные в secrets. Для этого нужно перейти в настройки репозитория Settings, выбрать на панели слева Secrets, нажать New secret и последовательно добавлять каждую переменную:
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
- запустить docker-compose:
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
</details>


## :hammer_and_wrench: Используемые технологии:

<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg" title="Django" alt="Django" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="Postgresql" alt="Postgresql" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/linux/linux-original.svg" title="Linux" alt="Linux" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/ubuntu/ubuntu-plain-wordmark.svg" title="Ubuntu" alt="Ubuntu" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/nginx/nginx-original.svg" title="Nginx" alt="Nginx" width="40" height="40"/>&nbsp; 
</div>
