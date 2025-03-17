from django.shortcuts import render
from django.http import HttpResponse
from main.models import Course
from django.db.models import Count

def homepage(request):
    # Сортируем курсы по количеству студентов (записей в Enrollment)
    popular_courses = Course.objects.annotate(num_students=Count('enrollments')).order_by('-num_students')[:6]

    context = {
        'courses': popular_courses
    }
    return render(request, 'main/home.html', context)
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

from django.shortcuts import render, get_object_or_404
from .models import Course

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    modules = course.modules.all()

    return render(request, 'main/course_detail.html', {'course': course, 'modules': modules})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from .forms import CourseForm

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'main/course_list.html', {'courses': courses})

@login_required
def dashboard(request):
    user = request.user

    if user.user_type == "teacher":
        courses = Course.objects.filter(teacher=user)
        return render(request, "main/teacher_dashboard.html", {"courses": courses})


    student = getattr(user, "student", None)
    if not student:
        return redirect("dashboard_setup")

    enrolled_courses = Enrollment.objects.filter(student=student).select_related("course")
    available_courses = Course.objects.exclude(enrollments__student=student)

    return render(request, "main/student_dashboard.html", {
        "enrolled_courses": enrolled_courses,
        "available_courses": available_courses
    })

from .models import Student, Teacher

def setup_profile(request):
    user = request.user

    if user.user_type == "student" and not hasattr(user, "student"):
        Student.objects.create(user=user)
    elif user.user_type == "teacher" and not hasattr(user, "teacher"):
        Teacher.objects.create(user=user)

    return redirect("dashboard")

@login_required
def create_course(request):
    if request.user.user_type != "teacher":
        return redirect("dashboard")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect("dashboard")
    else:
        form = CourseForm()

    return render(request, "main/create_course.html", {"form": form})


@login_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = CourseForm(instance=course)

    return render(request, "main/edit_course.html", {"form": form, "course": course})


@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)
    course.delete()
    return redirect("dashboard")


@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    Enrollment.objects.get_or_create(student=request.user.student, course=course)
    return redirect("dashboard")


