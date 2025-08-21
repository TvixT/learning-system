from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('instructor/courses/', views.instructor_courses, name='instructor_courses'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:pk>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:pk>/delete/', views.delete_course, name='delete_course'),
    path('course/<int:course_pk>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('course/<int:course_pk>/lessons/', views.course_lessons, name='course_lessons'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('employee/enrollments/', views.employee_enrollments, name='employee_enrollments'),
    path('course/<int:course_pk>/review/', views.submit_review, name='submit_review'),
    path('review/<int:review_pk>/approve/', views.approve_review, name='approve_review'),
    path('review/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    path('reviews/', views.review_list, name='review_list'),
]