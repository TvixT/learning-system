from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/users/', views.employee_user_management, name='employee_user_management'),
    path('employee/users/<int:user_id>/', views.employee_user_detail, name='employee_user_detail'),
]