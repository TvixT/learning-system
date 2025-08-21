from django.db import models
from django.urls import reverse
from courses.models import Course


class Lesson(models.Model):
    """
    Lesson model representing a lesson within a course.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    video_file = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    document = models.FileField(upload_to='lessons/documents/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'course_pk': self.course.pk, 'lesson_pk': self.pk})

    def get_video_source(self):
        """
        Return the video source URL, either from uploaded file or external URL.
        """
        if self.video_file:
            return self.video_file.url
        elif self.video_url:
            return self.video_url
        return None

    def is_video_external(self):
        """
        Check if the video is an external URL (e.g., YouTube, Vimeo).
        """
        if self.video_url:
            return True
        return False