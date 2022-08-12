release: python manage.py migrate --noinput
web: gunicorn --bind :$PORT --workers 5 --threads 2 --worker-class gthread core.wsgi