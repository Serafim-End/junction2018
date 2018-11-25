release: python manage.py migrate
web: gunicorn junction.wsgi --timeout 1200 --log-file -