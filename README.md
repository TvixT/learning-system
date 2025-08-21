# Online Learning System V3

A comprehensive online learning platform built with Python Django.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Setup](#project-setup)
4. [Default Users](#default-users)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Project Structure](#project-structure)
8. [Screenshots](#screenshots)

## Project Overview

The Online Learning System is a comprehensive platform that allows students to enroll in courses, instructors to create and manage course content, and employees to oversee the entire system. The platform includes features for course management, lesson delivery, assignments, progress tracking, and review systems.

## Features

### Phase 1: Authentication System
- Custom user model with role-based authentication (student, instructor, employee)
- User registration with role selection (limited to student/instructor)
- Login/logout functionality
- Role-based redirects to appropriate dashboards
- Responsive UI with dark theme using Tailwind CSS

### Phase 2: Course Management
- Course, Category, and Tag models for content organization
- Role-based course management:
  - Instructors can create, edit, and manage their own courses
  - Employees can manage all courses, categories, and tags
- Public course browsing with search and filtering capabilities

### Phase 3: Lesson Management
- Lesson model linked to Course with multimedia support
- Video content support (uploaded files or external URLs)
- Document upload capability (PDFs, docs, etc.)
- Lesson ordering for structured course progression
- Instructor lesson management within their courses

### Phase 4: Enrollment and Progress Tracking
- Enrollment model connecting students and courses
- Course browsing with filtering by category, tag, or instructor
- Student enrollment in courses with progress tracking
- Lesson completion tracking per enrollment
- Student dashboard showing enrolled courses and progress
- Employee interface to view and manage all enrollments

### Phase 5: User Dashboards
- Enhanced dashboards for all user roles:
  - Student Dashboard: enrolled courses, progress tracking, recent activity
  - Instructor Dashboard: course statistics, student enrollments, recent courses
  - Employee Dashboard: system-wide statistics, management shortcuts

### Phase 6: Assignment System
- Assignment model linked to lessons with title, description, due date, max score
- Submission model for student assignment submissions (file or text)
- Student assignment submission with validation and deadline enforcement
- Instructor grading interface with score and feedback capabilities
- Student grade viewing interface

### Phase 7: Review System
- Review model for students to rate and review courses
- Student review submission for completed courses
- Employee review moderation (approve/delete)
- Display of average ratings and reviews on course detail pages
- Validation to prevent multiple reviews per student per course

## Project Setup

1. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```
   python manage.py migrate
   ```

5. **Populate sample data:**
   ```
   python manage.py populate_courses_data
   python manage.py populate_lessons_data
   python manage.py populate_enrollments_data
   python manage.py populate_assignments_data
   python manage.py populate_reviews_data
   ```

6. **Create a superuser (optional):**
   ```
   python manage.py createsuperuser
   ```

## Default Users

The project includes sample users for testing:

| Role       | Username   | Password      |
|------------|------------|---------------|
| Student    | student    | password123   |
| Instructor | instructor | password123   |
| Instructor | instructor2| password123   |
| Employee   | employee   | password123   |
| Admin      | admin      | password123   |

## Running the Application

To start the development server:
```
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Testing

To run all tests:
```
python manage.py test
```

To run tests for a specific app:
```
python manage.py test accounts
python manage.py test courses
python manage.py test lessons
python manage.py test assignments
```

## Project Structure

```
online_learning_system/
├── accounts/                 # Authentication and user management
│   ├── models.py            # Custom user model
│   ├── views.py             # Authentication views
│   ├── forms.py             # Authentication forms
│   ├── urls.py              # Authentication URLs
│   ├── templates/           # Authentication templates
│   └── tests.py             # Authentication tests
├── courses/                 # Course management
│   ├── models.py            # Course, category, tag, enrollment, review models
│   ├── views.py             # Course views
│   ├── forms.py             # Course forms
│   ├── urls.py              # Course URLs
│   ├── templates/           # Course templates
│   └── tests.py             # Course tests
├── lessons/                 # Lesson management
│   ├── models.py            # Lesson model
│   ├── views.py             # Lesson views
│   ├── forms.py             # Lesson forms
│   ├── urls.py              # Lesson URLs
│   ├── templates/           # Lesson templates
│   └── tests.py             # Lesson tests
├── assignments/             # Assignment management
│   ├── models.py            # Assignment and submission models
│   ├── views.py             # Assignment views
│   ├── forms.py             # Assignment forms
│   ├── urls.py              # Assignment URLs
│   ├── templates/           # Assignment templates
│   └── tests.py             # Assignment tests
├── templates/               # Base templates
├── media/                   # Uploaded files
├── static/                  # Static files
├── docs/                    # Project documentation
├── requirements.txt         # Project dependencies
└── online_learning_system/  # Main project settings
    ├── settings.py          # Django settings
    ├── urls.py              # Main URLs
    └── wsgi.py              # WSGI configuration
```

## Screenshots

The `/screenshots` folder contains UI captures of the application:

- Home page
- Login and registration pages
- Student dashboard
- Instructor dashboard
- Employee dashboard
- Course listing and filtering
- Course detail page with reviews
- Lesson viewing and completion
- Assignment creation and submission
- Review submission and moderation

To view screenshots, navigate to the `/screenshots` directory in the project root.