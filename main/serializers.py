from rest_framework import serializers
from .models import CustomUser, Course, Module, Lesson, Enrollment, Certificate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type']

class CourseSerializer(serializers.ModelSerializer):
    teacher = CustomUserSerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'image', 'created_at']

class ModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'order']

class LessonSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()

    class Meta:
        model = Lesson
        fields = ['id', 'module', 'title', 'content_type', 'text_content', 'video_url', 'file', 'order']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']

class CertificateSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Certificate
        fields = ['id', 'student', 'course', 'certificate_file', 'issued_at']
