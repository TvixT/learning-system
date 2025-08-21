from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import make_password

User = get_user_model()


class AccountsTestCase(TestCase):
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

    def test_user_creation(self):
        """Test that users can be created with correct roles"""
        self.assertEqual(self.student_user.role, 'student')
        self.assertEqual(self.instructor_user.role, 'instructor')
        self.assertEqual(self.employee_user.role, 'employee')

    def test_user_role_display(self):
        """Test that get_role_display returns correct values"""
        self.assertEqual(self.student_user.get_role_display(), 'Student')
        self.assertEqual(self.instructor_user.get_role_display(), 'Instructor')
        self.assertEqual(self.employee_user.get_role_display(), 'Employee')

    def test_user_absolute_url(self):
        """Test that get_absolute_url returns correct URLs based on role"""
        self.assertEqual(self.student_user.get_absolute_url(), reverse('student_dashboard'))
        self.assertEqual(self.instructor_user.get_absolute_url(), reverse('instructor_dashboard'))
        self.assertEqual(self.employee_user.get_absolute_url(), reverse('employee_dashboard'))

    def test_login_view(self):
        """Test that users can log in"""
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_login_failure(self):
        """Test that login fails with incorrect credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Stay on login page
        self.assertContains(response, 'Invalid username or password.')

    def test_register_view_get(self):
        """Test that register page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_view_post(self):
        """Test that users can register"""
        response = self.client.post(reverse('register'), {
            'username': 'newstudent',
            'email': 'newstudent@test.com',
            'role': 'student',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newstudent').exists())