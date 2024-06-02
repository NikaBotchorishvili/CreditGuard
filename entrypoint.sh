#!/bin/sh

python manage.py migrate

python manage.py shell << END
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='demetre').exists():
    User.objects.create_superuser('demetre', 'chakvetadzedemetre@gmail.com', '12345678')
END

exec "$@"
