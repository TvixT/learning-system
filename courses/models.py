from django.db import models
from django.urls import reverse
from accounts.models import User


class Category(models.Model):
    """
    Category model for organizing courses.
    Managed by employees.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Tag model for categorizing courses with keywords.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Course model representing a course in the learning system.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    published = models.BooleanField(default=False)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})

    def get_lessons_count(self):
        """Return the total number of lessons in this course."""
        return self.lessons.count()

    def get_average_rating(self):
        """Calculate and return the average rating for this course."""
        reviews = self.reviews.filter(approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    def get_review_count(self):
        """Return the number of approved reviews for this course."""
        return self.reviews.filter(approved=True).count()


class Enrollment(models.Model):
    """
    Enrollment model connecting students and courses.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

    def get_progress(self):
        """Calculate the progress of this enrollment as a percentage."""
        total_lessons = self.course.get_lessons_count()
        if total_lessons == 0:
            return 0
        
        completed_lessons = self.lesson_completions.count()
        return int((completed_lessons / total_lessons) * 100)

    def get_completed_lessons_count(self):
        """Return the number of completed lessons for this enrollment."""
        return self.lesson_completions.count()


class LessonCompletion(models.Model):
    """
    Model to track completion of individual lessons by students.
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_completions')
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')
        ordering = ['completed_at']

    def __str__(self):
        return f"{self.enrollment.student.username} completed {self.lesson.title}"


class Review(models.Model):
    """
    Review model for students to review courses.
    """
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username}'s review for {self.course.title}"

    def get_rating_display_text(self):
        """Return the text description of the rating."""
        return dict(self.RATING_CHOICES)[self.rating]