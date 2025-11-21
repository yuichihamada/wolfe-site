release: python manage.py collectstatic --noinput
web: gunicorn wolfe_site.wsgi:application --bind 0.0.0.0:$PORT