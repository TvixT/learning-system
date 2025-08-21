from django.core.management.base import BaseCommand
from lessons.models import Lesson
from courses.models import Course


class Command(BaseCommand):
    help = 'Populate the database with sample lessons'

    def handle(self, *args, **options):
        # Get sample courses
        try:
            python_course = Course.objects.get(title='Complete Python Programming Course')
            django_course = Course.objects.get(title='Django for Beginners')
            js_course = Course.objects.get(title='Modern JavaScript Fundamentals')
            react_course = Course.objects.get(title='React Frontend Development')
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR('One or more sample courses not found. Please run create_sample_courses.py first.'))
            return

        # Create sample lessons for Python course
        python_lessons = [
            {
                'title': 'Introduction to Python',
                'description': 'Learn the basics of Python programming language.',
                'course': python_course,
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/_uQrJ0TkZlc'
            },
            {
                'title': 'Variables and Data Types',
                'description': 'Understanding variables and data types in Python.',
                'course': python_course,
                'order': 2,
                'video_url': 'https://www.youtube.com/embed/XmtHJrZqRLM'
            },
            {
                'title': 'Control Structures',
                'description': 'Learn about if statements, loops, and other control structures.',
                'course': python_course,
                'order': 3,
                'video_url': 'https://www.youtube.com/embed/TqPzwenhMj0'
            }
        ]

        # Create sample lessons for Django course
        django_lessons = [
            {
                'title': 'Introduction to Django',
                'description': 'Get started with Django web framework.',
                'course': django_course,
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/UmljCsHZKOM'
            },
            {
                'title': 'Models and Databases',
                'description': 'Learn how to work with models and databases in Django.',
                'course': django_course,
                'order': 2,
                'video_url': 'https://www.youtube.com/embed/m_aYKvZ42U8'
            }
        ]

        # Create sample lessons for JavaScript course
        js_lessons = [
            {
                'title': 'JavaScript Basics',
                'description': 'Learn the fundamentals of JavaScript.',
                'course': js_course,
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/W6NZfCO5SIk'
            },
            {
                'title': 'Functions and Scope',
                'description': 'Understanding functions and scope in JavaScript.',
                'course': js_course,
                'order': 2,
                'video_url': 'https://www.youtube.com/embed/pI1skOo2yjk'
            }
        ]

        # Create sample lessons for React course
        react_lessons = [
            {
                'title': 'React Components',
                'description': 'Learn about React components and props.',
                'course': react_course,
                'order': 1,
                'video_url': 'https://www.youtube.com/embed/Y2hgEGPzTZY'
            },
            {
                'title': 'State and Lifecycle',
                'description': 'Understanding state management and component lifecycle.',
                'course': react_course,
                'order': 2,
                'video_url': 'https://www.youtube.com/embed/cJwe4iV5q4o'
            },
            {
                'title': 'Hooks Introduction',
                'description': 'Learn about React Hooks and how to use them.',
                'course': react_course,
                'order': 3,
                'video_url': 'https://www.youtube.com/embed/f687hBjwFcM'
            }
        ]

        # Combine all lessons
        all_lessons = python_lessons + django_lessons + js_lessons + react_lessons

        # Create lessons
        for lesson_data in all_lessons:
            # Check if lesson already exists
            if not Lesson.objects.filter(title=lesson_data['title'], course=lesson_data['course']).exists():
                Lesson.objects.create(**lesson_data)
                self.stdout.write(f"Created lesson: {lesson_data['title']}")
            else:
                self.stdout.write(f"Lesson {lesson_data['title']} already exists")

        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample lessons')
        )