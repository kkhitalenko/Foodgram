# Foodgram
Foodgram - продуктовый помощник, онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Необходимые технологии: Docker, Docker-Compose

## Как запустить API локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:kkhitalenko/foodgram-project-react/
```

```
cd foodgram-project-react/
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

Загрузить имеющуюся базу данных для работы проекта:

```
python manage.py import_json
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

Перейти в папку backend/

```
cd backend/
```

Обновить менеджер пакетов pip

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Получить документацию:
- перейти в папку infra/

```
cd ../infra/
```

- выполнить команду:

```
docker-compose up
```

- документация и примеры запросов будут досупны по адресу:

```
http://localhost/api/docs/redoc.html
```


Используемые технологии: DRF, REST API, Redoc, Docker, Docker-Сompose, Docker Hub, Nginx, Gunicorn, Github Actions, Yandex.Cloud

