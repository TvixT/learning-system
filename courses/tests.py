from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Category, Tag, Course, Enrollment, Review
from lessons.models import Lesson

User = get_user_model()


class CoursesTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.student_user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123',
            role='student'
        )
        self.instructor_user = User.objects.create_user(
            username='testinstructor',
            email='instructor@test.com',
            password='testpass123',
            role='instructor'
        )
        self.employee_user = User.objects.create_user(
            username='testemployee',
            email='employee@test.com',
            password='testpass123',
            role='employee'
        )
        
        # Create test category and tag
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.tag = Tag.objects.create(
            name='Test Tag'
        )
        
        # Create test course
        self.course = Course.objects.create(
            title='Test Course',
            description='Test course description',
            price=99.99,
            instructor=self.instructor_user,
            category=self.category,
            published=True
        )
        self.course.tags.add(self.tag)
        
        # Create test lesson
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test lesson description',
            course=self.course,
            order=1
        )

    def test_course_creation(self):
        """Test that courses can be created"""
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.instructor, self.instructor_user)
        self.assertEqual(self.course.category, self.category)
        self.assertTrue(self.course.published)

    def test_course_lessons_count(self):
        """Test that get_lessons_count returns correct value"""
        self.assertEqual(self.course.get_lessons_count(), 1)

    def test_course_average_rating(self):
        """Test that get_average_rating returns correct value"""
        # Create a review
        Review.objects.create(
            course=self.course,
            student=self.student_user,
            rating=5,
            review_text='Great course!',
            approved=True
        )
        self.assertEqual(self.course.get_average_rating(), 5.0)

    def test_course_review_count(self):
        """Test that get_review_count returns correct value"""
        # Create a review
        Review.objects.create(
            course=self.course,
            student=self.student_user,
            rating=5,
            review_text='Great course!',
            approved=True
        )
        self.assertEqual(self.course.get_review_count(), 1)

    def test_enrollment_creation(self):
        """Test that enrollments can be created"""
        enrollment = Enrollment.objects.create(
            student=self.student_user,
            course=self.course
        )
        self.assertEqual(enrollment.student, self.student_user)
        self.assertEqual(enrollment.course, self.course)

    def test_enrollment_progress(self):
        """Test that get_progress returns correct value"""
        enrollment = Enrollment.objects.create(
            student=self.student_user,
            course=self.course
        )
        self.assertEqual(enrollment.get_progress(), 0)

    def test_course_list_view(self):
        """Test that course list page loads correctly"""
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_course_detail_view(self):
        """Test that course detail page loads correctly"""
        response = self.client.get(reverse('course_detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_instructor_courses_view(self):
        """Test that instructor courses page loads correctly"""
        self.client.login(username='testinstructor', password='testpass123')
        response = self.client.get(reverse('instructor_courses'))
        self.assertEqual(response.status_code, 200)

    def test_student_enrollment(self):
        """Test that students can enroll in courses"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.post(reverse('enroll_in_course', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after enrollment
        self.assertTrue(Enrollment.objects.filter(
            student=self.student_user,
            course=self.course
        ).exists())