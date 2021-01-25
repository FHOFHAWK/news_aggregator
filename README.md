## 1. Создание виртуального окружения
```sh
python -m venv env
```
## 2. Запуск виртуального окружения
```sh
env\Scripts\activate
```
## 3. Установка зависимостей
```sh
pip install -r requirements.txt
```
# Создание базы данных
```sh
create database django
```
# Создание пользователя 
```sh
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';

flush privileges
```
# Подключение базы данных в settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
# Миграции
```sh
python manage.py migrate
```
# Запуск проекта
```sh
python manage.py runserver
```
# Запуск redis в Docker
```sh
docker run -d -p 6379:6379 --name redis redis
```
# Запуск Celery worker
```sh
celery -A aggregator worker -l info
```