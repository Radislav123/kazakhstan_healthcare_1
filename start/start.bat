venv\scripts\python manage.py core_copy_chrome_profile >> logs\core\copy_chrome_profile.log 2>&1
venv\scripts\python manage.py eisz_log_in >> logs\eisz\log_in.log 2>&1
venv\scripts\python manage.py eisz_reports_download >> logs\eisz\reports_download.log 2>&1
venv\scripts\python manage.py damumed_log_in >> logs\damumed\log_in.log 2>&1
venv\scripts\python manage.py damumed_screenings_download >> logs\damumed\screenings_download.log 2>&1
venv\scripts\python manage.py damumed_unloadings_download >> logs\damumed\unloadings_download.log 2>&1
venv\scripts\python manage.py damumed_reports_download >> logs\damumed\reports_download.log 2>&1
