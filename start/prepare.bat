python -m venv venv
venv\scripts\pip install -r requirements.txt
venv\scripts\python manage.py makemigrations parser
venv\scripts\python manage.py migrate
venv\scripts\python manage.py prepare_db
