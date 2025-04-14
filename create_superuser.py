# create_superuser.py
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('demo', 'demo@example.com', 'demo')