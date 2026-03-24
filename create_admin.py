from django.contrib.auth import get_user_model
import django
import os
import sys

# Ensure project root is on sys.path so Django settings import works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glaucoma_project.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print('created')
else:
    print('exists')
