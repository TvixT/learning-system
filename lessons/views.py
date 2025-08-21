from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Lesson
from .forms import LessonForm
from courses.models import Course, Enrollment, LessonCompletion


@login_required
def lesson_list(request, course_pk):
    """
    Display a list of lessons for a specific course.
    """
    course = get_object_or_404(Course, pk=course_pk)
    
    # Check if the user is the instructor of this course or an employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    lessons = Lesson.objects.filter(course=course).order_by('order', 'created_at')
    
    # Pagination
    paginator = Paginator(lessons, 10)  # Show 10 lessons per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'lessons/lesson_list.html', {
        'course': course,
        'page_obj': page_obj
    })


@login_required
def lesson_detail(request, course_pk, lesson_pk):
    """
    Display details of a specific lesson.
    """
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Check access based on user role
    if request.user.role == 'student':
        # Students must be enrolled in the course
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.error(request, 'You must be enrolled in this course to view this lesson.')
            return redirect('course_detail', pk=course.pk)
    elif request.user.role == 'instructor':
        # Instructors must be the course instructor
        if course.instructor != request.user:
            messages.error(request, 'Access denied.')
            return redirect('home')
    elif request.user.role != 'employee':
        # Other roles are denied
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # For students, get completed lessons
    completed_lessons = set()
    if request.user.role == 'student':
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            completed_lessons = set(LessonCompletion.objects.filter(enrollment=enrollment).values_list('lesson_id', flat=True))
        except Enrollment.DoesNotExist:
            pass
    
    return render(request, 'lessons/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'completed_lessons': completed_lessons
    })


@login_required
def create_lesson(request, course_pk):
    """
    Allow instructors to create a new lesson for their course.
    """
    course = get_object_or_404(Course, pk=course_pk)
    
    # Check if the user is the instructor of this course or an employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lesson created successfully!')
            return redirect('lesson_list', course_pk=course.pk)
    else:
        form = LessonForm()
    
    return render(request, 'lessons/lesson_form.html', {
        'form': form,
        'course': course,
        'title': 'Create Lesson'
    })


@login_required
def edit_lesson(request, course_pk, lesson_pk):
    """
    Allow instructors to edit their own lessons.
    """
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Check if the user is the instructor of this course or an employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, 'Lesson updated successfully!')
            return redirect('lesson_detail', course_pk=course.pk, lesson_pk=lesson.pk)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'lessons/lesson_form.html', {
        'form': form,
        'course': course,
        'lesson': lesson,
        'title': 'Edit Lesson'
    })


@login_required
def delete_lesson(request, course_pk, lesson_pk):
    """
    Allow instructors to delete their own lessons.
    """
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    
    # Check if the user is the instructor of this course or an employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Lesson deleted successfully!')
        return redirect('lesson_list', course_pk=course.pk)
    
    return render(request, 'lessons/lesson_confirm_delete.html', {
        'course': course,
        'lesson': lesson
    })