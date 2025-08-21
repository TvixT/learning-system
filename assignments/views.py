from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, GradeSubmissionForm
from lessons.models import Lesson
from courses.models import Course, Enrollment
from django.utils import timezone


@login_required
def assignment_list(request):
    """
    Display a list of assignments for a specific lesson.
    """
    lesson_pk = request.GET.get('lesson')
    if not lesson_pk:
        messages.error(request, 'Lesson not specified.')
        return redirect('home')
    
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    course = lesson.course
    
    # Check if user has access to this lesson
    if request.user.role == 'student':
        # Check if student is enrolled in the course
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.error(request, 'You are not enrolled in this course.')
            return redirect('home')
    elif request.user.role == 'instructor':
        # Check if instructor owns this course
        if course.instructor != request.user:
            messages.error(request, 'You do not have permission to view this lesson.')
            return redirect('home')
    elif request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    assignments = Assignment.objects.filter(lesson=lesson)
    
    # Pagination
    paginator = Paginator(assignments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'assignments/assignment_list.html', {
        'lesson': lesson,
        'course': course,
        'page_obj': page_obj
    })


@login_required
def assignment_detail(request, pk):
    """
    Display details of a specific assignment.
    """
    assignment = get_object_or_404(Assignment, pk=pk)
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user has access to this assignment
    if request.user.role == 'student':
        # Check if student is enrolled in the course
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.error(request, 'You are not enrolled in this course.')
            return redirect('home')
    elif request.user.role == 'instructor':
        # Check if instructor owns this course
        if course.instructor != request.user:
            messages.error(request, 'You do not have permission to view this assignment.')
            return redirect('home')
    elif request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get submission if student
    submission = None
    if request.user.role == 'student':
        try:
            submission = Submission.objects.get(assignment=assignment, student=request.user)
        except Submission.DoesNotExist:
            submission = None
    
    return render(request, 'assignments/assignment_detail.html', {
        'assignment': assignment,
        'lesson': lesson,
        'course': course,
        'submission': submission
    })


@login_required
def create_assignment(request, lesson_pk):
    """
    Allow instructors to create a new assignment for a lesson.
    """
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    course = lesson.course
    
    # Check if user is instructor of this course or employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'You do not have permission to create assignments for this lesson.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.lesson = lesson
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm()
    
    return render(request, 'assignments/assignment_form.html', {
        'form': form,
        'lesson': lesson,
        'course': course,
        'title': 'Create Assignment'
    })


@login_required
def edit_assignment(request, pk):
    """
    Allow instructors to edit an assignment.
    """
    assignment = get_object_or_404(Assignment, pk=pk)
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user is instructor of this course or employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'You do not have permission to edit this assignment.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(request, 'assignments/assignment_form.html', {
        'form': form,
        'lesson': lesson,
        'course': course,
        'assignment': assignment,
        'title': 'Edit Assignment'
    })


@login_required
def delete_assignment(request, pk):
    """
    Allow instructors to delete an assignment.
    """
    assignment = get_object_or_404(Assignment, pk=pk)
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user is instructor of this course or employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'You do not have permission to delete this assignment.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('assignment_list', lesson=lesson.pk)
    
    return render(request, 'assignments/assignment_confirm_delete.html', {
        'assignment': assignment,
        'lesson': lesson,
        'course': course
    })


@login_required
def submit_assignment(request, assignment_pk):
    """
    Allow students to submit an assignment.
    """
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user is a student
    if request.user.role != 'student':
        messages.error(request, 'Only students can submit assignments.')
        return redirect('home')
    
    # Check if student is enrolled in the course
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('home')
    
    # Check if assignment is overdue
    if assignment.is_overdue():
        messages.error(request, 'This assignment is overdue and cannot be submitted.')
        return redirect('assignment_detail', pk=assignment.pk)
    
    # Check if student has already submitted
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.error(request, 'You have already submitted this assignment.')
        return redirect('assignment_detail', pk=assignment.pk)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = SubmissionForm()
    
    return render(request, 'assignments/submission_form.html', {
        'form': form,
        'assignment': assignment,
        'lesson': lesson,
        'course': course,
        'title': 'Submit Assignment'
    })


@login_required
def grade_submission(request, submission_pk):
    """
    Allow instructors to grade a submission.
    """
    submission = get_object_or_404(Submission, pk=submission_pk)
    assignment = submission.assignment
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user is instructor of this course or employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'You do not have permission to grade this submission.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission, assignment=assignment)
        if form.is_valid():
            submission = form.save()
            messages.success(request, 'Submission graded successfully!')
            return redirect('submission_detail', pk=submission.pk)
    else:
        form = GradeSubmissionForm(instance=submission, assignment=assignment)
    
    return render(request, 'assignments/grade_submission.html', {
        'form': form,
        'submission': submission,
        'assignment': assignment,
        'lesson': lesson,
        'course': course,
        'title': 'Grade Submission'
    })


@login_required
def submission_detail(request, pk):
    """
    Display details of a specific submission.
    """
    submission = get_object_or_404(Submission, pk=pk)
    assignment = submission.assignment
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user has access to this submission
    if request.user.role == 'student' and submission.student != request.user:
        messages.error(request, 'You do not have permission to view this submission.')
        return redirect('home')
    elif request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'You do not have permission to view this submission.')
        return redirect('home')
    elif request.user.role not in ['student', 'instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    return render(request, 'assignments/submission_detail.html', {
        'submission': submission,
        'assignment': assignment,
        'lesson': lesson,
        'course': course
    })


@login_required
def assignment_submissions(request, assignment_pk):
    """
    Display all submissions for an assignment (for instructors).
    """
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    lesson = assignment.lesson
    course = lesson.course
    
    # Check if user is instructor of this course or employee
    if request.user.role == 'instructor' and course.instructor != request.user:
        messages.error(request, 'You do not have permission to view submissions for this assignment.')
        return redirect('home')
    elif request.user.role not in ['instructor', 'employee']:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    submissions = Submission.objects.filter(assignment=assignment)
    
    # Pagination
    paginator = Paginator(submissions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'assignments/submission_list.html', {
        'assignment': assignment,
        'lesson': lesson,
        'course': course,
        'page_obj': page_obj
    })