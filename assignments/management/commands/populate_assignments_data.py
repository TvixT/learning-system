from django.core.management.base import BaseCommand
from assignments.models import Assignment
from lessons.models import Lesson
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate the database with sample assignments'

    def handle(self, *args, **options):
        # Get sample lessons
        lessons = Lesson.objects.all()[:5]  # Get first 5 lessons
        
        if not lessons.exists():
            self.stdout.write(self.style.ERROR('No lessons found. Please create lessons first.'))
            return
        
        # Create sample assignments
        assignment_data = [
            {
                'title': 'Python Basics Assignment',
                'description': 'Complete the exercises on variables, data types, and basic operations.',
                'lesson': lessons[0],
                'due_date': timezone.now() + timedelta(days=7),
                'max_score': 100
            },
            {
                'title': 'Django Models Exercise',
                'description': 'Create models for a blog application with posts, comments, and tags.',
                'lesson': lessons[1],
                'due_date': timezone.now() + timedelta(days=10),
                'max_score': 100
            },
            {
                'title': 'JavaScript Functions Practice',
                'description': 'Write functions to solve the provided problems using JavaScript.',
                'lesson': lessons[2],
                'due_date': timezone.now() + timedelta(days=5),
                'max_score': 100
            },
            {
                'title': 'React Components Assignment',
                'description': 'Build reusable React components for a user dashboard.',
                'lesson': lessons[3],
                'due_date': timezone.now() + timedelta(days=14),
                'max_score': 100
            }
        ]
        
        # Create assignments
        for data in assignment_data:
            lesson = data.pop('lesson')
            # Check if assignment already exists
            if not Assignment.objects.filter(title=data['title'], lesson=lesson).exists():
                Assignment.objects.create(lesson=lesson, **data)
                self.stdout.write(f"Created assignment: {data['title']}")
            else:
                self.stdout.write(f"Assignment {data['title']} already exists")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample assignments')
        )