from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """
    Custom User model with role-based authentication.
    """
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('employee', 'Employee'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    def get_absolute_url(self):
        if self.role == 'student':
            return reverse('student_dashboard')
        elif self.role == 'instructor':
            return reverse('instructor_dashboard')
        elif self.role == 'employee':
            return reverse('employee_dashboard')
        else:
            return reverse('home')  # fallback URL
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class StudentProfile(models.Model):
    """
    Profile model for students with additional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=20, unique=True)
    enrollment_date = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Student Profile"


class InstructorProfile(models.Model):
    """
    Profile model for instructors with additional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Instructor Profile"


class EmployeeProfile(models.Model):
    """
    Profile model for employees with additional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Employee Profile"