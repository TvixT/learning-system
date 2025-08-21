from django import forms
from .models import Assignment, Submission
from django.core.exceptions import ValidationError
from django.utils import timezone


class AssignmentForm(forms.ModelForm):
    """
    Form for creating and editing assignments.
    """
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_score']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_due_date(self):
        """
        Validate that the due date is in the future.
        """
        due_date = self.cleaned_data['due_date']
        if due_date <= timezone.now():
            raise ValidationError("Due date must be in the future.")
        return due_date


class SubmissionForm(forms.ModelForm):
    """
    Form for submitting assignments.
    """
    class Meta:
        model = Submission
        fields = ['file', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        """
        Validate that either file or text is provided, but not both.
        """
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        text = cleaned_data.get('text')

        if file and text:
            raise ValidationError("Please provide either a file or text, not both.")

        if not file and not text:
            raise ValidationError("Please provide either a file or text.")

        return cleaned_data


class GradeSubmissionForm(forms.ModelForm):
    """
    Form for instructors to grade submissions.
    """
    class Meta:
        model = Submission
        fields = ['score', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment', None)
        super().__init__(*args, **kwargs)
        if self.assignment:
            self.fields['score'].widget.attrs.update({
                'max': self.assignment.max_score,
                'min': 0
            })

    def clean_score(self):
        """
        Validate that the score is within the allowed range.
        """
        score = self.cleaned_data['score']
        if self.assignment and score is not None:
            if score > self.assignment.max_score:
                raise ValidationError(f"Score cannot be higher than {self.assignment.max_score}.")
            if score < 0:
                raise ValidationError("Score cannot be negative.")
        return score