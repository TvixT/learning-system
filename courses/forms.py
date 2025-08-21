from django import forms
from .models import Course, Category, Tag
from django.forms.widgets import CheckboxSelectMultiple


class CourseForm(forms.ModelForm):
    """
    Form for creating and editing courses.
    """
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'image', 'published', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-surface-2 border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'e.g., Mastering React for Beginners'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-surface-2 border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent min-h-[120px]',
                'placeholder': 'What learners will build, prerequisites, and outcomes.',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-surface-2 border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-surface-2 border border-border rounded-lg text-text focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent'
            }),
            'image': forms.FileInput(attrs={
                'class': 'hidden'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'rounded text-accent focus:ring-accent'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'hidden'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category optional
        self.fields['category'].required = False
        # Add empty label for category
        self.fields['category'].empty_label = "Select category"
        # Limit tags queryset if needed
        self.fields['tags'].queryset = Tag.objects.all()