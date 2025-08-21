from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import User
from courses.models import Category, Course, Enrollment, LessonCompletion
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    """
    Handle user login with role-based redirects.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user role
            return redirect(user.get_absolute_url())
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def register_view(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect(user.get_absolute_url())
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def home_view(request):
    """
    Home page view with featured courses and categories.
    """
    # Get featured courses (published courses ordered by most recent)
    featured_courses = Course.objects.filter(published=True).select_related(
        'instructor', 'category'
    ).prefetch_related('tags').order_by('-created_at')[:6]
    
    # Get all categories with course counts
    categories = Category.objects.annotate(
        courses=Count('course')
    ).filter(courses__gt=0)[:8]
    
    # Get system stats
    stats = {
        'courses': Course.objects.filter(published=True).count(),
        'students': User.objects.filter(role='student').count(),
        'instructors': User.objects.filter(role='instructor').count(),
        'enrollments': Enrollment.objects.count(),
    }
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'stats': stats,
    }
    
    return render(request, 'accounts/home.html', context)


def student_dashboard(request):
    """
    Student dashboard view with enrolled courses and progress.
    """
    if request.user.is_authenticated and request.user.role == 'student':
        # Get student's enrollments with related course and lesson completion data
        enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__instructor')
        
        # Calculate overall progress
        total_courses = enrollments.count()
        completed_courses = enrollments.filter(completed=True).count()
        
        # Get recent enrollments
        recent_enrollments = enrollments.order_by('-enrolled_at')[:3]
        
        context = {
            'enrollments': enrollments,
            'total_courses': total_courses,
            'completed_courses': completed_courses,
            'recent_enrollments': recent_enrollments,
        }
        
        return render(request, 'accounts/student_dashboard.html', context)
    else:
        messages.error(request, 'Access denied.')
        return redirect('login')


def instructor_dashboard(request):
    """
    Instructor dashboard view with course statistics.
    """
    if request.user.is_authenticated and request.user.role == 'instructor':
        # Get instructor's courses
        courses = Course.objects.filter(instructor=request.user).prefetch_related('enrollments')
        
        # Calculate statistics
        total_courses = courses.count()
        total_enrollments = sum(course.enrollments.count() for course in courses)
        
        # Get recent courses
        recent_courses = courses.order_by('-created_at')[:3]
        
        # Get enrollment data for chart
        enrollment_data = []
        for course in courses:
            enrollment_data.append({
                'title': course.title,
                'enrollments': course.enrollments.count()
            })
        
        context = {
            'courses': courses,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'recent_courses': recent_courses,
            'enrollment_data': enrollment_data,
        }
        
        return render(request, 'accounts/instructor_dashboard.html', context)
    else:
        messages.error(request, 'Access denied.')
        return redirect('login')


def employee_dashboard(request):
    """
    Employee dashboard view with system statistics.
    """
    if request.user.is_authenticated and request.user.role == 'employee':
        # Get system statistics
        total_students = User.objects.filter(role='student').count()
        total_instructors = User.objects.filter(role='instructor').count()
        total_courses = Course.objects.count()
        total_enrollments = Enrollment.objects.count()
        
        # Get recent activity
        recent_courses = Course.objects.select_related('instructor').order_by('-created_at')[:5]
        recent_enrollments = Enrollment.objects.select_related('student', 'course').order_by('-enrolled_at')[:5]
        
        # Get enrollment trend (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        enrollment_trend = Enrollment.objects.filter(
            enrolled_at__gte=thirty_days_ago
        ).extra(select={'date': 'date(enrolled_at)'}).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        context = {
            'total_students': total_students,
            'total_instructors': total_instructors,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'recent_courses': recent_courses,
            'recent_enrollments': recent_enrollments,
            'enrollment_trend': list(enrollment_trend),
        }
        
        return render(request, 'accounts/employee_dashboard.html', context)
    else:
        messages.error(request, 'Access denied.')
        return redirect('login')


@login_required
def employee_user_management(request):
    """
    Employee user management view.
    """
    if request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get all users with related profile information
    users = User.objects.all().select_related(
        'studentprofile', 
        'instructorprofile', 
        'employeeprofile'
    ).order_by('-date_joined')
    
    # Filter by role if specified
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'role_filter': role_filter,
    }
    
    return render(request, 'accounts/employee_user_management.html', context)


@login_required
def employee_user_detail(request, user_id):
    """
    Employee user detail view for managing user roles.
    """
    if request.user.role != 'employee':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get the user with related profile information
    user = get_object_or_404(User.objects.select_related(
        'studentprofile', 
        'instructorprofile', 
        'employeeprofile'
    ), id=user_id)
    
    if request.method == 'POST':
        # Update user role
        new_role = request.POST.get('role')
        if new_role in dict(User.ROLE_CHOICES):
            user.role = new_role
            user.save()
            messages.success(request, f'User role updated to {user.get_role_display()}.')
            return redirect('employee_user_detail', user_id=user.id)
        else:
            messages.error(request, 'Invalid role selected.')
    
    context = {
        'user_detail': user,
    }
    
    return render(request, 'accounts/employee_user_detail.html', context)