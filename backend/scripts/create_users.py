"""
Create additional test users for the system
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Define test users
test_users = [
    {
        'username': 'john_doe',
        'email': 'john.doe@example.com',
        'password': 'john123',
        'first_name': 'John',
        'last_name': 'Doe',
        'is_staff': True,
        'is_superuser': False
    },
    {
        'username': 'jane_smith',
        'email': 'jane.smith@example.com',
        'password': 'jane123',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'is_staff': True,
        'is_superuser': False
    },
    {
        'username': 'engineer1',
        'email': 'engineer1@example.com',
        'password': 'eng123',
        'first_name': 'Alice',
        'last_name': 'Engineer',
        'is_staff': False,
        'is_superuser': False
    },
    {
        'username': 'analyst1',
        'email': 'analyst1@example.com',
        'password': 'analyst123',
        'first_name': 'Bob',
        'last_name': 'Analyst',
        'is_staff': False,
        'is_superuser': False
    }
]

print("Creating test users...\n")
print("=" * 70)

created_count = 0
skipped_count = 0

for user_data in test_users:
    username = user_data['username']
    
    if User.objects.filter(username=username).exists():
        print(f"⚠️  User '{username}' already exists - skipping")
        skipped_count += 1
    else:
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        
        role = "Admin Staff" if user.is_staff else "Regular User"
        print(f"✅ Created: {username:15} | {role:15} | Password: {password}")
        created_count += 1

print("=" * 70)
print(f"\n📊 Summary:")
print(f"   Created: {created_count} users")
print(f"   Skipped: {skipped_count} users (already exist)")
print(f"   Total users in system: {User.objects.count()}")

print("\n" + "=" * 70)
print("USER CREDENTIALS:")
print("=" * 70)
print(f"{'Username':<15} {'Password':<15} {'Role':<20} {'Email'}")
print("-" * 70)
print(f"{'admin':<15} {'admin123':<15} {'Superuser':<20} {'admin@example.com'}")
print(f"{'john_doe':<15} {'john123':<15} {'Staff':<20} {'john.doe@example.com'}")
print(f"{'jane_smith':<15} {'jane123':<15} {'Staff':<20} {'jane.smith@example.com'}")
print(f"{'engineer1':<15} {'eng123':<15} {'Regular User':<20} {'engineer1@example.com'}")
print(f"{'analyst1':<15} {'analyst123':<15} {'Regular User':<20} {'analyst1@example.com'}")
print("=" * 70)

print("\n💡 TIP: Staff users can access admin panel at /admin/")
print("💡 TIP: All users can use the API with Basic Authentication")
print("\n✅ All users ready to use!")
