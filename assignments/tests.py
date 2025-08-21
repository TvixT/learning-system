from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from courses.models import Category, Course, Enrollment
from lessons.models import Lesson
from assignments.models import Assignment
from datetime import timedelta

User = get_user_model()


class AssignmentsTestCase(TestCase):
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
        
        # Create test category, course, and lesson
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
        
        # Create test assignment with due_date
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            description='Test assignment description',
            lesson=self.lesson,
            due_date=timezone.now() + timedelta(days=7),
            max_score=100
        )

    def test_assignment_creation(self):
        """Test that assignments can be created"""
        self.assertEqual(self.assignment.title, 'Test Assignment')
        self.assertEqual(self.assignment.lesson, self.lesson)
        self.assertEqual(self.assignment.max_score, 100)

    def test_assignment_absolute_url(self):
        """Test that get_absolute_url returns correct URL"""
        expected_url = reverse('assignment_detail', kwargs={'pk': self.assignment.pk})
        self.assertEqual(self.assignment.get_absolute_url(), expected_url)

    def test_assignment_list_view(self):
        """Test that assignment list page loads correctly"""
        self.client.login(username='testinstructor', password='testpass123')
        response = self.client.get(reverse('assignment_list') + f'?lesson={self.lesson.pk}')
        self.assertEqual(response.status_code, 200)

    def test_assignment_detail_view(self):
        """Test that assignment detail page loads correctly"""
        self.client.login(username='testinstructor', password='testpass123')
        response = self.client.get(reverse('assignment_detail', kwargs={'pk': self.assignment.pk}))
        self.assertEqual(response.status_code, 200)

    def test_student_assignment_access(self):
        """Test that students can access assignments for enrolled courses"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('assignment_list') + f'?lesson={self.lesson.pk}')
        self.assertEqual(response.status_code, 200)