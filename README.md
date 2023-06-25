# Проект Foodgram [![foodgram_workflow](https://github.com/MelodiousWarbler/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)](https://github.com/MelodiousWarbler/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

### Описание проекта:

Foodgram, «Продуктовый помощник».
На этом сервисе пользователи могут публиковать рецепты,
подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное»,
а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

Проект развёрнут по адресу: http://foodgramm.hopto.org:1996/

---

### Стек технологий:

- Python 3.9.16
- Django 2.2.28
- Django rest framework 3.11
- Djoser 2.0.4
- Gunicorn
- Nginx
- PostgreSQL
- Git
- Docker

---

### Получение проекта:

Форк репозитория с GitHab:

```commandline
https://github.com/MelodiousWarbler/foodgram-project-react.git
```

---

### Запуск проекта локально в Docker-контейнерах:

Ручное заполнение файла '.env':

```text
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
POSTGRES_DB=postgres                        # имя базы данных
POSTGRES_USER=postgres                  # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres              # пароль для подключения к БД (установите свой)
DB_HOST=db                              # название сервиса (контейнера)
DB_PORT=5432                            # порт для подключения к БД
ALLOWED_HOSTS=localhost                 # локальный хост, 127.0.0.1, [::1] или *
```

Выполнить команду развертывания контейнеров проекта:

```commandline
docker-compose up -d
```

---

### Запуск проекта на сервере:

#### Подготовка GitHub Actions:

После создания репозитория в своем аккаунте GitHub во вкладке настроек
репозитория проекта, в меню выбрать `Secrets and variables` выбрать `Actions`,
нажать кнопку `New repository secret`, создать переменные окружения:

| Секрет               | Значение                                                                               |
|----------------------|----------------------------------------------------------------------------------------|
| SECRET_KEY           | "секретный ключ джанго-проекта" в кавычках                                             |
| ALLOWED_HOSTS        | *, хост сервера                                                                        |
| DOCKER_USERNAME      | имя пользователя в DockerHub                                                           |
| DOCKER_PASSWORD      | пароль доступа в DockerHub                                                             |
| DB_ENGINE            | django.db.backends.postgresql                                                          |
| POSTGRES_DB          | имя базы данных                                                                        |
| POSTGRES_USER        | логин для подключения к базе данных                                                    |
| POSTGRES_PASSWORD    | пароль для подключения к БД                                                            |
| DB_HOST              | db                                                                                     |
| DB_PORT              | 5432                                                                                   |
| USER                 | логин сервера                                                                          |
| HOST                 | ip сервера                                                                             |
| SSH_KEY              | приватный ключ локальной машины, по которому происходит вход на сервер (~/.ssh/id_rsa) |
| PASSPHRASE           | фраза-пароль ключа ssh (если установлена)                                              |
| TELEGRAM_TO          | id телеграм-чата (@userinfobot)                                                        |
| TELEGRAM_TOKEN       | токен телеграм-бота (@BotFather - /mybots - Choose a bot - API Token)                  |


#### Подготовка сервера:

Войти на свой удаленный сервер.
Установить Docker и docker-compose.

```commandline
sudo apt install docker.io
```

```commandline
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```commandline
sudo chmod +x /usr/local/bin/docker-compose
```

Из паки `infra` локального проекта cкопировать на сервер в домашнюю дирректорию
файлы настроек nginx и docker-compose

```commandline
scp docker-compose.yaml <USER>@<HOST>:/home/<USER>
```

```commandline
scp nginx.conf <USER>@<HOST>:/home/<USER>
```

Запуск при любом `push` на GitHub проект:
- тестируется на соответствие PEP8, 
- обновляются и сохраняются на DockerHub образы `backend` и `frontend`, 
- в домашней директории сервера автоматически создается файл `.env`
- проект автоматически разворачивается на сервере, 
- о чем приходит сообщение на telegram.

Для запуска сервиса на сервере вручную:
- на сервере в домашней директории создать файл `.env` с настройками
по образцу выше с учетом данных хоста.

```commandline
nano .env
```

- запуск

```commandline
sudo docker-compose up -d
```

--- 
После успешного развертывания проекта на сервере или локально:
Выполнить миграции, создать суперпользователя, собрать статику

```commandline
sudo docker-compose exec backend python manage.py migrate
```

```commandline
sudo docker-compose exec backend python manage.py createsuperuser
```

```commandline
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Для подгрузки в базу данных ингредиентов:

```commandline
sudo docker-compose exec backend python manage.py load_data
```

В админ-зоне проекта создать необходимые теги

---

### Работа с сервисом:

Сервис будет доступен:

при локальном развертывании - http://localhost/

При развертывании на сервере - http://<ip_адрес_хоста>/

Доступ к административной части: <host>/admin
Доступ к API: <host>/api
Спецификация API: <host>/api/docs

---

### Разработка проекта:

Бэкенд, логика сервиса, соединение с подготовленным фронтендом, CI/CD проекта:
Яков Плакотнюк https://github.com/MelodiousWarbler
