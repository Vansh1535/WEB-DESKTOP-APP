"""
Create default preferences for existing users
Run with: python manage.py shell < create_default_preferences.py
"""
from django.contrib.auth.models import User
from users.models import UserPreferences

# Get all users without preferences
users_without_prefs = User.objects.filter(preferences__isnull=True)

print(f"Creating preferences for {users_without_prefs.count()} users...")

for user in users_without_prefs:
    UserPreferences.objects.create(user=user)
    print(f"Created preferences for user: {user.username}")

print("Done!")
