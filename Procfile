release: python manage.py migrate --no-input
web: python manage.py collectstatic --no-input && gunicorn --workers 3 --bind 0.0.0.0:$PORT config.wsgi:application