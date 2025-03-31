from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Teacher

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "student"
        if commit:
            user.save()
            Student.objects.create(user=user)
        return user

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "teacher"
        if commit:
            user.save()
            Teacher.objects.create(user=user)
        return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user_type = cleaned_data.get("user_type")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            if user.user_type != user_type:
                raise forms.ValidationError("User type mismatch")

        return cleaned_data

from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "image"]

from django import forms
from .models import Module, Lesson

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title"]


from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content_type", "text_content", "video_url", "file"]


