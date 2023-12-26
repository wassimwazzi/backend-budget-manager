web: gunicorn backend.wsgi
worker: python manage.py run_huey
release: python manage.py migrate