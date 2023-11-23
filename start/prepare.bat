python -m venv venv
venv\scripts\pip install -r requirements.txt
venv\scripts\python manage.py makemigrations core, eisz, damumed
venv\scripts\python manage.py migrate
venv\scripts\python manage.py core_create_admin
venv\scripts\python manage.py core_prepare_db
venv\scripts\python manage.py eisz_prepare_db
venv\scripts\python manage.py damumed_prepare_db
