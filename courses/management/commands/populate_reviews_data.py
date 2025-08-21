from django.core.management.base import BaseCommand
from courses.models import Review, Course, Enrollment
from accounts.models import User
import random


class Command(BaseCommand):
    help = 'Populate the database with sample reviews'

    def handle(self, *args, **options):
        # Get sample students and courses
        students = User.objects.filter(role='student')
        courses = Course.objects.filter(published=True)
        
        if not students.exists() or not courses.exists():
            self.stdout.write(self.style.ERROR('Students or courses not found. Please create them first.'))
            return
        
        # Create sample reviews
        review_texts = [
            "This course was incredibly helpful! I learned so much and the instructor was great.",
            "Good content but could use more practical examples.",
            "Excellent course with clear explanations and useful assignments.",
            "The course material was well-structured and easy to follow.",
            "I enjoyed this course and would recommend it to others.",
            "Very informative and well-presented. Helped me advance my skills.",
            "Great course overall, though some sections felt a bit rushed.",
            "Outstanding content and teaching style. Highly recommended!",
            "This course exceeded my expectations. Very comprehensive.",
            "Good introduction to the topic but could be more in-depth."
        ]
        
        # Create reviews for each enrollment
        for enrollment in Enrollment.objects.all():
            # 70% chance of creating a review
            if random.random() < 0.7:
                # Check if review already exists
                if not Review.objects.filter(student=enrollment.student, course=enrollment.course).exists():
                    review = Review.objects.create(
                        course=enrollment.course,
                        student=enrollment.student,
                        rating=random.randint(3, 5),  # Most reviews are positive
                        review_text=random.choice(review_texts),
                        approved=True  # Approved for demo purposes
                    )
                    self.stdout.write(f"Created review: {review.student.username} for {review.course.title}")
                else:
                    self.stdout.write(f"Review already exists: {enrollment.student.username} for {enrollment.course.title}")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample reviews')
        )