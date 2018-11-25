release: python manage.py migrate
web: gunicorn junction.wsgi --log-file --max-requests 1000 --timeout 100