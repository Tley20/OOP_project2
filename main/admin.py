from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student, Teacher

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "user_type", "is_active", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("User Type", {"fields": ("user_type",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ("user",)
    search_fields = ("user__username", "user__email")

class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ("user", "subject", "job_title")
    search_fields = ("user__username", "user__email", "subject", "job_title")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)


