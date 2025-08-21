from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for our custom User model.
    Users can only register as students or instructors.
    Employees are assigned by admins.
    """
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='student')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')