release: python manage.py migrate
web: gunicorn junction.wsgi --timeout 1500 --keep-alive 5 --log-file -