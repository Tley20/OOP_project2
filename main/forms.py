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
        fields = ["username", "email", "password1", "password2", "subject", "job_title"]

    subject = forms.CharField(max_length=100, required=True)
    job_title = forms.CharField(max_length=100, required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "teacher"
        if commit:
            user.save()
            # Достаем subject и job_title из self.cleaned_data
            Teacher.objects.create(user=user, subject=self.cleaned_data["subject"], job_title=self.cleaned_data["job_title"])
        return user

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser  # Импортируем кастомную модель пользователя

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

