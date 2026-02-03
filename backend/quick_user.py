import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Delete if exists
User.objects.filter(username='test').delete()

# Create test user
user = User.objects.create_user(username='test', email='test@test.com', password='test')
print("✅ Test user created!")
print("Username: test")
print("Password: test")
