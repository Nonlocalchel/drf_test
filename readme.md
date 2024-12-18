<h2 align="center">TaskService by Django</h2>

Typical проект фриланс биржы на Django Rest Framework.<br>
Тест: https://github.com/Nonlocalchel/drf_test/blob/main/manual.md
### Инструменты разработки

**Стек:**
- Python >= 3.8
- Django Rest Framework
- Postgres
- Redis

## Старт

#### 1) Создать образ

    docker-compose build

##### 2) Запустить контейнер

    docker-compose up
    
##### 3) Перейти по адресу

    http://127.0.0.1:8000/api/v1/swagger/
## Разработка с Docker

##### 1) Сделать форк репозитория

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) В корне проекта создать .env.prod и .env.prod.db

- .env.prod:
    ```
    DEBUG=0
    SECRET_KEY=some_secret_key
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
    REDIS_URL=redis://redis:6379/0
    REDIS_PASSWORD=pines
    ```
- .env.prod.db:
    ```
    POSTGRES_DB=your_db_name
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=your_db_host
    ```
    
##### 4) Создать образ

    docker-compose build

##### 5) Запустить контейнер

    docker-compose up
    
##### 6) Создать суперюзера

    docker exec -it backend python manage.py createsuperuser
                     
##### 8) Если нужно очистить БД

    docker-compose down -v
## Unit - тесты
- Запустить все тесты:
  ```
    docker exec backend python manage.py test
  ```
- Для приложения user:
  ```
    docker exec backend python manage.py test users
  ```
- Для приложения task:
  ```
    docker exec backend python manage.py test tasks
  ```