from django.shortcuts import render
from django.http import HttpResponse
from main.models import Course
from django.db.models import Count

def homepage(request):
    popular_courses = Course.objects.annotate(num_students=Count('enrollments')).order_by('-num_students')[:6]

    context = {
        'courses': popular_courses
    }
    return render(request, 'main/home.html', context)

def register_choice(request):
    return render(request, "main/register.html")

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

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    modules = course.modules.all()

    enrolled = False
    if request.user.is_authenticated and request.user.user_type == "student":
        enrolled = Enrollment.objects.filter(student__user=request.user, course=course).exists()

    return render(request, 'main/course_detail.html', {
        'course': course,
        'modules': modules,
        'enrolled': enrolled
    })
from django.contrib.auth.decorators import login_required
from .models import  Enrollment
from django.contrib import messages
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'main/course_list.html', {'courses': courses})

from django.db.models import Count

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

    course_progress = []
    total_lessons = 0
    total_completed = 0

    for enrollment in enrolled_courses:
        course = enrollment.course
        lessons = Lesson.objects.filter(module__course=course).count()
        completed_lessons = CompletedLesson.objects.filter(student=student, lesson__module__course=course).count()

        progress = (completed_lessons / lessons * 100) if lessons > 0 else 0
        total_lessons += lessons
        total_completed += completed_lessons

        course_progress.append({
            "course": course,
            "progress": round(progress, 2)
        })

    overall_progress = (total_completed / total_lessons * 100) if total_lessons > 0 else 0

    return render(request, "main/student_dashboard.html", {
        "course_progress": course_progress,
        "overall_progress": round(overall_progress, 2),
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
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)


    student = get_object_or_404(Student, user=request.user)


    enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)

    if created:
        messages.success(request, f"You have successfully enrolled in {course.title}!")
    else:
        messages.warning(request, "You are already enrolled in this course.")

    return redirect("course_detail", pk=course.id)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Lesson, CompletedLesson, Student
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CompleteLessonView(View):
    def post(self, request, lesson_id):
        student = get_object_or_404(Student, user=request.user)
        lesson = get_object_or_404(Lesson, id=lesson_id)

        completed, created = CompletedLesson.objects.get_or_create(student=student, lesson=lesson)

        if created:
            return JsonResponse({"message": "Lesson marked as completed"}, status=200)
        else:
            return JsonResponse({"message": "Lesson already completed"}, status=400)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Module, Lesson
from .forms import CourseForm, ModuleForm, LessonForm

@login_required
def create_module(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect("course_detail", pk=course.id)
    else:
        form = ModuleForm()

    return render(request, "main/create_module.html", {"form": form, "course": course})

@login_required
def create_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__teacher=request.user)

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect("course_detail", pk=module.course.id)
    else:
        form = LessonForm()

    return render(request, "main/create_lesson.html", {"form": form, "module": module})


@login_required
def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__teacher=request.user)

    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect("course_detail", pk=module.course.id)
    else:
        form = ModuleForm(instance=module)

    return render(request, "main/edit_module.html", {"form": form, "module": module})


@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__teacher=request.user)
    course_id = module.course.id
    module.delete()
    return redirect("course_detail", pk=course_id)

@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__teacher=request.user)

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect("course_detail", pk=lesson.module.course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, "main/edit_lesson.html", {"form": form, "lesson": lesson})

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__teacher=request.user)
    course_id = lesson.module.course.id
    lesson.delete()
    return redirect("course_detail", pk=course_id)


from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Certificate, CompletedLesson, Student, Course, Lesson
import os


@login_required
def generate_certificate(request, course_id):
    student = get_object_or_404(Student, user=request.user)
    course = get_object_or_404(Course, id=course_id)

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = CompletedLesson.objects.filter(student=student, lesson__module__course=course).count()

    if completed_lessons < total_lessons:
        messages.error(request, "You must complete all lessons to receive a certificate.")
        return redirect("course_detail", pk=course.id)

    certificate, created = Certificate.objects.get_or_create(student=student, course=course)

    if certificate.certificate_file:
        try:
            return FileResponse(certificate.certificate_file.open(), as_attachment=True,
                                filename=f"certificate_{course.title}.pdf")
        except ValueError:
            pass

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4

    pdf.setFillColor(black)

    logo_path = "static/logo.png"
    if os.path.exists(logo_path):
        pdf.drawImage(logo_path, 50, page_height - 100, width=120, height=60, mask='auto')

    pdf.setFont("Helvetica-Bold", 28)
    title = "COURSE CERTIFICATE"
    text_width = pdf.stringWidth(title, "Helvetica-Bold", 28)
    pdf.drawString((page_width - text_width) / 2, 720, title)

    pdf.setFillColor(HexColor("#E0E0E0"))
    pdf.rect(page_width - 120, 550, 100, 170, fill=True, stroke=False)
    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(page_width - 110, 680, "COURSE")
    pdf.drawString(page_width - 110, 660, "CERTIFICATE")

    pdf.setFont("Helvetica", 18)
    pdf.drawString(100, 600, "Presented to:")
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(100, 570, student.user.username)

    pdf.setFont("Helvetica", 18)
    pdf.drawString(100, 530, "For successfully completing:")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(100, 500, course.title)

    pdf.setFont("Helvetica", 16)
    pdf.drawString(100, 460, f"Issued on: {certificate.issued_at.strftime('%d-%m-%Y')}")

    pdf.line(100, 370, 250, 370)
    pdf.line(300, 370, 450, 370)

    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, 350, f"Instructor: {course.teacher.username}")
    pdf.drawString(300, 350, "Course Coordinator")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    certificate.certificate_file.save(f"certificate_{course.title}.pdf", ContentFile(buffer.read()))
    buffer.close()

    return FileResponse(certificate.certificate_file.open(), as_attachment=True,
                        filename=f"certificate_{course.title}.pdf")






