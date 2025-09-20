release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
web: gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application