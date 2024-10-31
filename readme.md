<h2 align="center">TaskService by Django</h2>

Typical проект фриланс биржы на Django Rest Framework.

### Инструменты разработки

**Стек:**
- Python >= 3.8
- Django Rest Framework
- Postgres

## Старт

#### 1) Создать образ

    docker-compose build

##### 2) Запустить контейнер

    docker-compose up
    
##### 3) Перейти по адресу

    http://127.0.0.1:8000/api/v1/swagger/

## Сервис 
 Чтобы воспольоваться сервисом понадобиться создать учетные записи, либо воспользоваться fixtures

И воспользоваться учетными данными(username, password):
- Работник(c extra permissions): (worker_1, worker_super_ps_387)
- Заказчик: (customer_1, customer_super_ps_387)

Для того чтобы взаимодействовать с документацие надо либо авторизоваться, либо получить jwt-токен и подставить его

Вы не можете создать свой аккаунт в системе, это может сделать только worker with extra permissions
## Разработка с Docker

##### 1) Сделать форк репозитория

##### 2) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 3) В корне проекта создать .env

    SECRET_KEY=some_secret_key
    POSTGRES_DB=some_task_service_db
    POSTGRES_USER=some_django_task_service_admin
    POSTGRES_PASSWORD=some_task_password_3234
    
##### 4) Создать образ

    docker-compose build

##### 5) Запустить контейнер

    docker-compose up
    
##### 6) Создать суперюзера

    docker-compose run --rm backend sh -c "
	DJANGO_SUPERUSER_USERNAME=admin2 DJANGO_SUPERUSER_PASSWORD=psw \
    python manage.py createsuperuser --email=admin@admin.com --noinput"
                                   
##### 7) создаем миграции и мигрируем
    
    docker-compose run --rm backend sh -c "python manage.py makemigrations"    
    docker-compose run --rm backend sh -c "python manage.py migrate"
                     
##### 8) Если нужно очистить БД

    docker-compose down -v