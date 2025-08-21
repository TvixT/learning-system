from django.contrib import admin
from .models import Category, Tag, Course, Enrollment, LessonCompletion, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag model.
    """
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for Course model.
    """
    list_display = ('title', 'instructor', 'category', 'price', 'published', 'created_at')
    list_filter = ('category', 'tags', 'published', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'instructor__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)
    
    # Allow employees to manage all courses
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Employees can see all courses
        if request.user.role == 'employee':
            return qs
        # Instructors can only see their own courses
        elif request.user.role == 'instructor':
            return qs.filter(instructor=request.user)
        # Students cannot see courses in admin
        return qs.none
    
    # Restrict course creation based on user role
    def has_add_permission(self, request):
        # Only instructors and employees can add courses
        return request.user.role in ['instructor', 'employee']
    
    # Restrict course changes based on user role
    def has_change_permission(self, request, obj=None):
        # Employees can change any course
        if request.user.role == 'employee':
            return True
        # Instructors can only change their own courses
        if request.user.role == 'instructor' and obj is not None:
            return obj.instructor == request.user
        # Students cannot change courses
        return False
    
    # Restrict course deletion based on user role
    def has_delete_permission(self, request, obj=None):
        # Employees can delete any course
        if request.user.role == 'employee':
            return True
        # Instructors can only delete their own courses
        if request.user.role == 'instructor' and obj is not None:
            return obj.instructor == request.user
        # Students cannot delete courses
        return False


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Enrollment model.
    """
    list_display = ('student', 'course', 'enrolled_at', 'completed', 'completion_date')
    list_filter = ('completed', 'enrolled_at', 'completion_date')
    search_fields = ('student__username', 'course__title')
    ordering = ('-enrolled_at',)
    readonly_fields = ('enrolled_at', 'completion_date')
    
    # Allow employees to manage all enrollments
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Employees can see all enrollments
        if request.user.role == 'employee':
            return qs
        # Others cannot see enrollments in admin
        return qs.none
    
    # Restrict enrollment management based on user role
    def has_add_permission(self, request):
        # Only employees can add enrollments in admin
        return request.user.role == 'employee'
    
    # Restrict enrollment changes based on user role
    def has_change_permission(self, request, obj=None):
        # Only employees can change enrollments
        return request.user.role == 'employee'
    
    # Restrict enrollment deletion based on user role
    def has_delete_permission(self, request, obj=None):
        # Only employees can delete enrollments
        return request.user.role == 'employee'


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    """
    Admin configuration for LessonCompletion model.
    """
    list_display = ('enrollment', 'lesson', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('enrollment__student__username', 'lesson__title')
    ordering = ('-completed_at',)
    readonly_fields = ('completed_at',)
    
    # Allow employees to manage all lesson completions
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Employees can see all lesson completions
        if request.user.role == 'employee':
            return qs
        # Others cannot see lesson completions in admin
        return qs.none
    
    # Restrict lesson completion management based on user role
    def has_add_permission(self, request):
        # Only employees can add lesson completions in admin
        return request.user.role == 'employee'
    
    # Restrict lesson completion changes based on user role
    def has_change_permission(self, request, obj=None):
        # Only employees can change lesson completions
        return request.user.role == 'employee'
    
    # Restrict lesson completion deletion based on user role
    def has_delete_permission(self, request, obj=None):
        # Only employees can delete lesson completions
        return request.user.role == 'employee'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for Review model.
    """
    list_display = ('course', 'student', 'rating', 'approved', 'created_at')
    list_filter = ('rating', 'approved', 'created_at')
    search_fields = ('course__title', 'student__username', 'review_text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        """Approve selected reviews."""
        queryset.update(approved=True)
        self.message_user(request, f"{queryset.count()} reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        """Disapprove selected reviews."""
        queryset.update(approved=False)
        self.message_user(request, f"{queryset.count()} reviews disapproved.")
    disapprove_reviews.short_description = "Disapprove selected reviews"
    
    # Allow employees to manage all reviews
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Employees can see all reviews
        if request.user.role == 'employee':
            return qs
        # Others cannot see reviews in admin
        return qs.none
    
    # Restrict review management based on user role
    def has_add_permission(self, request):
        # Only employees can add reviews in admin
        return request.user.role == 'employee'
    
    # Restrict review changes based on user role
    def has_change_permission(self, request, obj=None):
        # Only employees can change reviews
        return request.user.role == 'employee'
    
    # Restrict review deletion based on user role
    def has_delete_permission(self, request, obj=None):
        # Only employees can delete reviews
        return request.user.role == 'employee'