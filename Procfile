release: python manage.py migrate
web: newrelic-admin run-program gunicorn junction.wsgi --max-requests 1000 --timeout 100 --preload