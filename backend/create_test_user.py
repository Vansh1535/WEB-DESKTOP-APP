"""
Quick script to create a test user
Run: python manage.py shell < create_test_user.py
"""
from django.contrib.auth.models import User

username = "admin"
password = "admin123"
email = "admin@example.com"

# Delete if exists
User.objects.filter(username=username).delete()

# Create new user
user = User.objects.create_user(username=username, email=email, password=password)
print(f"✅ Test user created!")
print(f"Username: {username}")
print(f"Password: {password}")
