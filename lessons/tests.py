from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Category, Course, Enrollment
from lessons.models import Lesson

User = get_user_model()


class LessonsTestCase(TestCase):
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
        
        # Create test category and course
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test course description',
            price=99.99,
            instructor=self.instructor_user,
            category=self.category,
            published=True
        )
        
        # Create test lesson
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test lesson description',
            course=self.course,
            order=1
        )
        
        # Create enrollment
        self.enrollment = Enrollment.objects.create(
            student=self.student_user,
            course=self.course
        )

    def test_lesson_creation(self):
        """Test that lessons can be created"""
        self.assertEqual(self.lesson.title, 'Test Lesson')
        self.assertEqual(self.lesson.course, self.course)
        self.assertEqual(self.lesson.order, 1)

    def test_lesson_absolute_url(self):
        """Test that get_absolute_url returns correct URL"""
        expected_url = reverse('lesson_detail', kwargs={
            'course_pk': self.course.pk,
            'lesson_pk': self.lesson.pk
        })
        self.assertEqual(self.lesson.get_absolute_url(), expected_url)

    def test_lesson_list_view(self):
        """Test that lesson list page loads correctly for instructor"""
        self.client.login(username='testinstructor', password='testpass123')
        response = self.client.get(reverse('lesson_list', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 200)

    def test_lesson_detail_view(self):
        """Test that lesson detail page loads correctly for instructor"""
        self.client.login(username='testinstructor', password='testpass123')
        response = self.client.get(reverse('lesson_detail', kwargs={
            'course_pk': self.course.pk,
            'lesson_pk': self.lesson.pk
        }))
        self.assertEqual(response.status_code, 200)

    def test_student_lesson_access(self):
        """Test that students can access lessons for enrolled courses"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('lesson_detail', kwargs={
            'course_pk': self.course.pk,
            'lesson_pk': self.lesson.pk
        }))
        self.assertEqual(response.status_code, 200)