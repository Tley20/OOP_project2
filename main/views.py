from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(request, "main/home.html", )

from django.shortcuts import redirect

def register_choice(request):
    return render(request, "main/register.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentRegistrationForm, TeacherRegistrationForm

def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")
    else:
        form = StudentRegistrationForm()
    return render(request, "main/register_student.html", {"form": form})

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")
    else:
        form = TeacherRegistrationForm()
    return render(request, "main/register_instructor.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomLoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect("homepage")  # Если пользователь уже вошел, редиректим

    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("homepage")
    else:
        form = CustomLoginForm()

    return render(request, "main/login.html", {"form": form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("homepage")



