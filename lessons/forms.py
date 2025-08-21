from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):
    """
    Form for creating and editing lessons.
    """
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'video_file', 'video_url', 'document', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make video_file and video_url optional
        self.fields['video_file'].required = False
        self.fields['video_url'].required = False
        self.fields['document'].required = False

    def clean(self):
        """
        Validate that either video_file or video_url is provided, but not both.
        """
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        video_url = cleaned_data.get('video_url')

        if video_file and video_url:
            raise forms.ValidationError("Please provide either a video file or a video URL, not both.")

        if not video_file and not video_url:
            raise forms.ValidationError("Please provide either a video file or a video URL.")

        return cleaned_data