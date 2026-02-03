"""
Quick script to create a test user for desktop app
"""
import os
import sys
import django

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserPreferences

def create_test_users():
    """Create test users"""
    
    # User 1: admin
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        UserPreferences.objects.create(user=user)
        print("✅ Created user: admin / admin123")
    else:
        print("ℹ️  User 'admin' already exists")
    
    # User 2: test
    if not User.objects.filter(username='test').exists():
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        UserPreferences.objects.create(user=user)
        print("✅ Created user: test / test123")
    else:
        print("ℹ️  User 'test' already exists")
    
    # User 3: demo
    if not User.objects.filter(username='demo').exists():
        user = User.objects.create_user(
            username='demo',
            email='demo@example.com',
            password='demo123',
            first_name='Demo',
            last_name='User'
        )
        UserPreferences.objects.create(user=user)
        print("✅ Created user: demo / demo123")
    else:
        print("ℹ️  User 'demo' already exists")
    
    print("\n" + "="*50)
    print("Test users ready! Use any of these to login:")
    print("="*50)
    print("1. Username: admin  | Password: admin123")
    print("2. Username: test   | Password: test123")
    print("3. Username: demo   | Password: demo123")
    print("="*50)

if __name__ == '__main__':
    create_test_users()
