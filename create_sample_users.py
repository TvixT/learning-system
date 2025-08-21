import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_learning_system.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.hashers import make_password

# Create sample users for each role
users_data = [
    {
        'username': 'student',
        'email': 'student@example.com',
        'password': 'password123',
        'role': 'student'
    },
    {
        'username': 'instructor',
        'email': 'instructor@example.com',
        'password': 'password123',
        'role': 'instructor'
    },
    {
        'username': 'employee',
        'email': 'employee@example.com',
        'password': 'password123',
        'role': 'employee'
    },
    {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'password123',
        'role': 'employee'  # Admin is an employee
    }
]

for user_data in users_data:
    # Check if user already exists
    if not User.objects.filter(username=user_data['username']).exists():
        # Create user
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )
        print(f"Created user: {user.username} with role: {user.role}")
    else:
        print(f"User {user_data['username']} already exists")

# Make admin a superuser
try:
    admin_user = User.objects.get(username='admin')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    print("Made admin user a superuser")
except User.DoesNotExist:
    print("Admin user not found")