from django.db import models
from django.urls import reverse
from lessons.models import Lesson
from accounts.models import User


class Assignment(models.Model):
    """
    Assignment model linked to a lesson.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    max_score = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} ({self.lesson.title})"

    def get_absolute_url(self):
        return reverse('assignment_detail', kwargs={'pk': self.pk})

    def is_overdue(self):
        """
        Check if the assignment is overdue.
        """
        from django.utils import timezone
        return timezone.now() > self.due_date


class Submission(models.Model):
    """
    Submission model for student assignment submissions.
    """
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='assignments/submissions/', blank=True, null=True)
    text = models.TextField(blank=True)
    score = models.PositiveIntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username}'s submission for {self.assignment.title}"

    def get_absolute_url(self):
        return reverse('submission_detail', kwargs={'pk': self.pk})

    def is_graded(self):
        """
        Check if the submission has been graded.
        """
        return self.score is not None