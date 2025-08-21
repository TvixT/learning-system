from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_pk>/lessons/', views.lesson_list, name='lesson_list'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/', views.lesson_detail, name='lesson_detail'),
    path('course/<int:course_pk>/lesson/create/', views.create_lesson, name='create_lesson'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/edit/', views.edit_lesson, name='edit_lesson'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/delete/', views.delete_lesson, name='delete_lesson'),
]