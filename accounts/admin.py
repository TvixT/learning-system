from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, InstructorProfile, EmployeeProfile


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for our User model with role field.
    """
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


# Register our models
admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)
admin.site.register(EmployeeProfile)