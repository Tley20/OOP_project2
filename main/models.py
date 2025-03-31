from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)


from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses")
    image = models.ImageField(upload_to="course_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):

    MODULE_CONTENT_CHOICES = [
        ("text", "Text"),
        ("video", "Video"),
        ("quiz", "Quiz"),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10, choices=MODULE_CONTENT_CHOICES, default="text")
    text_content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to="lesson_files/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.module.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:
            last_lesson = Lesson.objects.filter(module=self.module).order_by("-order").first()
            self.order = (last_lesson.order + 1) if last_lesson else 1
        super().save(*args, **kwargs)

    def get_embed_url(self):
        if self.video_url and "youtube.com/watch?v=" in self.video_url:
            return self.video_url.replace("watch?v=", "embed/")
        elif self.video_url and "youtu.be/" in self.video_url:
            video_id = self.video_url.split("youtu.be/")[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url

class CompletedLesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="completed_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="completed_by")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.user.username} completed {self.lesson.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.user.username} -> {self.course.title}"

from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from io import BytesIO

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    certificate_file = models.FileField(upload_to="certificates/")
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')




