from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from .models import Course, Category, Tag, Enrollment, LessonCompletion, Review
from accounts.models import User
from .forms import CourseForm
from lessons.models import Lesson


def course_list(request):
    """
    Display a list of published courses.
    """
    courses = Course.objects.filter(published=True).select_related('instructor', 'category').prefetch_related('tags')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(instructor__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)
    
    # Tag filter
    tag_id = request.GET.get('tag')
    if tag_id:
        courses = courses.filter(tags__id=tag_id)
    
    # Instructor filter
    instructor_id = request.GET.get('instructor')
    if instructor_id:
        courses = courses.filter(instructor_id=instructor_id)
    
    # Pagination
    paginator = Paginator(courses, 6)  # Show 6 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories, tags, and instructors for filter dropdowns
    categories = Category.objects.all()
    tags = Tag.objects.all()
    instructors = User.objects.filter(role='instructor')
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'instructors': instructors,
        'query': query,
        'selected_category': int(category_id) if category_id else None,
        'selected_tag': int(tag_id) if tag_id else None,
        'selected_instructor': int(instructor_id) if instructor_id else None,
    }
    
    return render(request, 'courses/course_list.html', context)


def course_detail(request, pk):
    """
    Display details of a specific course.
    """
    course = get_object_or_404(Course, pk=pk)
    
    # Check if student is enrolled in this course
    enrollment = None
    has_submitted_review = False
    
    if request.user.is_authenticated and request.user.role == 'student':
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            # Check if student has already submitted a review
            has_submitted_review = Review.objects.filter(student=request.user, course=course).exists()
        except Enrollment.DoesNotExist:
            enrollment = None
    
    # Get approved reviews for this course
    approved_reviews = Review.objects.filter(course=course, approved=True).select_related('student').order_by('-created_at')
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'has_submitted_review': has_submitted_review,
        'approved_reviews': approved_reviews
    })


@login_required
def instructor_courses(request):
    """
    Display courses created by the logged-in instructor.
    """
    if request.user.role != 'instructor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user).select_related('category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(courses, 5)  # Show 5 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'courses/instructor_courses.html', {'page_obj': page_obj})


@login_required
def create_course(request):
    """
    Allow instructors to create a new course.
    """
    if request.user.role != 'instructor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form_redesign.html', {'form': form, 'title': 'Create Course'})


@login_required
def edit_course(request, pk):
    """
    Allow instructors to edit their own courses.
    """
    course = get_object_or_404(Course, pk=pk)
    
    # Check if the user is the instructor of this course or an employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form_redesign.html', {
        'form': form, 
        'title': 'Edit Course',
        'course': course
    })


@login_required
def delete_course(request, pk):
    """
    Allow instructors to delete their own courses.
    """
    course = get_object_or_404(Course, pk=pk)
    
    # Check if the user is the instructor of this course or an employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        if request.user.role == 'instructor':
            return redirect('instructor_courses')
        else:
            return redirect('course_list')
    
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


@login_required
def enroll_in_course(request, course_pk):
    """
    Allow students to enroll in a course.
    """
    if request.user.role != 'student':
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('course_list')
    
    course = get_object_or_404(Course, pk=course_pk)
    
    # Check if student is already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('course_detail', pk=course.pk)
    
    # Create enrollment
    Enrollment.objects.create(student=request.user, course=course)
    messages.success(request, f'You have been enrolled in {course.title}!')
    
    return redirect('course_detail', pk=course.pk)


@login_required
def student_dashboard(request):
    """
    Display the student dashboard with enrolled courses and progress.
    """
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get student's enrollments with related course and lesson completion data
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__instructor')
    
    return render(request, 'courses/student_dashboard.html', {'enrollments': enrollments})


@login_required
def course_lessons(request, course_pk):
    """
    Display lessons for an enrolled course.
    """
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    course = get_object_or_404(Course, pk=course_pk)
    
    # Check if student is enrolled in this course
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'You must be enrolled in this course to view its lessons.')
        return redirect('course_detail', pk=course.pk)
    
    # Get lessons for this course
    lessons = Lesson.objects.filter(course=course).order_by('order', 'created_at')
    
    # Get completed lessons for this enrollment
    completed_lessons = LessonCompletion.objects.filter(enrollment=enrollment).values_list('lesson_id', flat=True)
    
    return render(request, 'courses/course_lessons.html', {
        'course': course,
        'lessons': lessons,
        'enrollment': enrollment,
        'completed_lessons': set(completed_lessons)
    })


@login_required
def mark_lesson_complete(request, course_pk, lesson_pk):
    """
    Mark a lesson as complete for a student.
    """
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Check if student is enrolled in this course
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'You must be enrolled in this course to mark lessons as complete.')
        return redirect('course_detail', pk=course.pk)
    
    # Create lesson completion if it doesn't exist
    LessonCompletion.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    
    # Check if course is now complete
    total_lessons = course.get_lessons_count()
    completed_lessons = enrollment.get_completed_lessons_count()
    
    if total_lessons > 0 and completed_lessons >= total_lessons and not enrollment.completed:
        enrollment.completed = True
        enrollment.save()
        messages.success(request, f'Congratulations! You have completed the course "{course.title}"!')
    else:
        messages.success(request, f'Lesson "{lesson.title}" marked as complete!')
    
    return redirect('course_lessons', course_pk=course.pk)


@login_required
def employee_enrollments(request):
    """
    Allow employees to view and manage all enrollments.
    """
    if request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    
    # Pagination
    paginator = Paginator(enrollments, 10)  # Show 10 enrollments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'courses/employee_enrollments.html', {'page_obj': page_obj})


@login_required
def submit_review(request, course_pk):
    """
    Allow students to submit a review for a course they're enrolled in.
    """
    course = get_object_or_404(Course, pk=course_pk)
    
    # Check if user is a student
    if request.user.role != 'student':
        messages.error(request, 'Only students can submit reviews.')
        return redirect('course_detail', pk=course.pk)
    
    # Check if student is enrolled in the course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in this course to submit a review.')
        return redirect('course_detail', pk=course.pk)
    
    # Check if student has already submitted a review
    if Review.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You have already submitted a review for this course.')
        return redirect('course_detail', pk=course.pk)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        # Validate rating
        if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
            messages.error(request, 'Please select a valid rating.')
            return render(request, 'courses/submit_review.html', {
                'course': course,
                'rating': rating,
                'review_text': review_text
            })
        
        # Validate review text
        if not review_text or len(review_text.strip()) < 10:
            messages.error(request, 'Review text must be at least 10 characters long.')
            return render(request, 'courses/submit_review.html', {
                'course': course,
                'rating': rating,
                'review_text': review_text
            })
        
        # Create review
        Review.objects.create(
            course=course,
            student=request.user,
            rating=int(rating),
            review_text=review_text.strip(),
            approved=False  # Reviews need to be approved by employees
        )
        
        messages.success(request, 'Your review has been submitted and is pending approval.')
        return redirect('course_detail', pk=course.pk)
    
    return render(request, 'courses/submit_review.html', {'course': course})


@login_required
def approve_review(request, review_pk):
    """
    Allow employees to approve a review.
    """
    review = get_object_or_404(Review, pk=review_pk)
    
    # Check if user is an employee
    if request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        review.approved = True
        review.save()
        messages.success(request, 'Review approved successfully.')
        return redirect('review_list')
    
    return render(request, 'courses/approve_review.html', {'review': review})


@login_required
def delete_review(request, review_pk):
    """
    Allow employees to delete a review.
    """
    review = get_object_or_404(Review, pk=review_pk)
    
    # Check if user is an employee
    if request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('review_list')
    
    return render(request, 'courses/delete_review.html', {'review': review})


@login_required
def review_list(request):
    """
    Display a list of reviews for employees to moderate.
    """
    # Check if user is an employee
    if request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    reviews = Review.objects.select_related('course', 'student').all()
    
    return render(request, 'courses/review_list.html', {'reviews': reviews})