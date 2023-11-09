# Установка

1) установить [*python 3.11*](https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe)
2) скачать [*проект*](https://github.com/Radislav123/kazakhstan_healthcare_1):
    ```shell
    git clone https://github.com/Radislav123/kazakhstan_healthcare_1.git
    ```
3) подготовить БД:
    ```shell
    python manage.py makemigrations parser
    python manage.py migrate
    python manage.py prepare_db
    ```
