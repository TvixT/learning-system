from django.core.management.base import BaseCommand
from courses.models import Enrollment
from accounts.models import User
from courses.models import Course
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate the database with sample enrollments'

    def handle(self, *args, **options):
        # Get sample students
        students = User.objects.filter(role='student')
        if not students.exists():
            self.stdout.write(self.style.ERROR('No students found. Please create student users first.'))
            return

        # Get sample courses
        courses = Course.objects.filter(published=True)
        if not courses.exists():
            self.stdout.write(self.style.ERROR('No published courses found. Please create courses first.'))
            return

        # Create sample enrollments
        for student in students:
            # Each student enrolls in 2-4 random courses
            num_enrollments = random.randint(2, 4)
            enrolled_courses = random.sample(list(courses), min(num_enrollments, len(courses)))

            for course in enrolled_courses:
                # Check if enrollment already exists
                if not Enrollment.objects.filter(student=student, course=course).exists():
                    enrollment = Enrollment.objects.create(
                        student=student,
                        course=course
                    )
                    self.stdout.write(f"Created enrollment: {student.username} in {course.title}")
                else:
                    self.stdout.write(f"Enrollment already exists: {student.username} in {course.title}")

        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample enrollments')
        )