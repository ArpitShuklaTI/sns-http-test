web: gunicorn live_sentiment_backend.wsgi
web: daphne -b 0.0.0.0 -p $PORT live_sentiment_backend.asgi:application
release: python manage.py makemigrations --noinput
release: python manage.py migrate --noinput
