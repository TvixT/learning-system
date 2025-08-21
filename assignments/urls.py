from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment_list'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('lesson/<int:lesson_pk>/assignment/create/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:pk>/edit/', views.edit_assignment, name='edit_assignment'),
    path('assignment/<int:pk>/delete/', views.delete_assignment, name='delete_assignment'),
    path('assignment/<int:assignment_pk>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_pk>/grade/', views.grade_submission, name='grade_submission'),
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail'),
    path('assignment/<int:assignment_pk>/submissions/', views.assignment_submissions, name='assignment_submissions'),
]