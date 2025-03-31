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
    list_display = ("user",)
    search_fields = ("user__username", "user__email")

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)


from django.utils.html import format_html
from .models import Course, Module, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "created_at", "course_image")
    search_fields = ("title", "teacher__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    fields = ("title", "description", "teacher", "image")

    def course_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit:cover;"/>', obj.image.url)
        return "No Image"

    course_image.allow_tags = True
    course_image.short_description = "Preview"


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_editable = ("order",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "content_type", "order")
    list_editable = ("order", "content_type")
    search_fields = ("title", "module__title")
    list_filter = ("content_type",)


from .models import  CompletedLesson, Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("get_student_username", "course", "enrolled_at")
    search_fields = ("student__user__username", "course__title")
    list_filter = ("enrolled_at",)

    def get_student_username(self, obj):
        return obj.student.user.username
    get_student_username.admin_order_field = "student__user__username"
    get_student_username.short_description = "Student"
admin.site.register(CompletedLesson)

from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "issued_at")
    search_fields = ("student__user__username", "course__title")
    list_filter = ("issued_at",)

