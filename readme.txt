1.endpoints:
    1.tasks:
       /api/v1/tasks/{number} - one task
       /api/v1/tasks - list task
       /api/v1/tasks/{number}/close-task - close-task

    2.users:
        /api/v1/customers/{number} - one task
        /api/v1/customers - list task
        /api/v1/workers/{number} - one task
        /api/v1/workers - list task

2.settings:
    AUTH_USER_MODEL = 'users.User'

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'users.apps.UsersConfig',
    'tasks.apps.TasksConfig'
    ]

3.REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )

    ...
}

остальные настройки стандартные