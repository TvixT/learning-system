import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_learning_system.settings')
django.setup()

from courses.models import Course, Category, Tag
from accounts.models import User

# Get sample users
try:
    instructor1 = User.objects.get(username='instructor')
    instructor2 = User.objects.create_user(
        username='instructor2',
        email='instructor2@example.com',
        password='password123',
        role='instructor'
    )
except User.DoesNotExist:
    print("Instructor user not found")
    exit(1)

# Get sample categories and tags
programming_category = Category.objects.get(name='Programming')
web_dev_category = Category.objects.get(name='Web Development')

python_tag = Tag.objects.get(name='Python')
django_tag = Tag.objects.get(name='Django')
javascript_tag = Tag.objects.get(name='JavaScript')
react_tag = Tag.objects.get(name='React')

# Create sample courses
courses_data = [
    {
        'title': 'Complete Python Programming Course',
        'description': 'Learn Python from basics to advanced topics including OOP, data structures, and more.',
        'price': 99.99,
        'instructor': instructor1,
        'category': programming_category,
        'tags': [python_tag],
        'published': True
    },
    {
        'title': 'Django for Beginners',
        'description': 'Build web applications with Django, the powerful Python web framework.',
        'price': 149.99,
        'instructor': instructor1,
        'category': web_dev_category,
        'tags': [python_tag, django_tag],
        'published': True
    },
    {
        'title': 'Modern JavaScript Fundamentals',
        'description': 'Master JavaScript fundamentals including ES6+ features, DOM manipulation, and async programming.',
        'price': 89.99,
        'instructor': instructor2,
        'category': programming_category,
        'tags': [javascript_tag],
        'published': True
    },
    {
        'title': 'React Frontend Development',
        'description': 'Build modern user interfaces with React, including hooks, context, and state management.',
        'price': 129.99,
        'instructor': instructor2,
        'category': web_dev_category,
        'tags': [javascript_tag, react_tag],
        'published': True
    }
]

for course_data in courses_data:
    # Check if course already exists
    if not Course.objects.filter(title=course_data['title']).exists():
        # Get tags before creating course
        tags = course_data.pop('tags')
        
        # Create course
        course = Course.objects.create(**course_data)
        
        # Add tags
        course.tags.set(tags)
        
        print(f"Created course: {course.title}")
    else:
        print(f"Course {course_data['title']} already exists")

print("Sample courses created successfully")