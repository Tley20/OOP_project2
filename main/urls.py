from django.urls import path
from . import views
from .views import login_view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('register', views.register_choice, name='register'),
    path("register/student/", views.register_student, name="register_student"),
    path("register/teacher/", views.register_teacher, name="register_instructor"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/setup/", views.setup_profile, name="dashboard_setup"),
    path("course/create/", views.create_course, name="create_course"),
    path("course/<int:pk>/edit/", views.edit_course, name="edit_course"),
    path("course/<int:pk>/delete/", views.delete_course, name="delete_course"),
    path('courses/', views.course_list, name='course_list'),
    path("course/<int:course_id>/enroll/", views.enroll_in_course, name="enroll_course"),
    path('course/<int:course_id>/module/add/', views.create_module, name='create_module'),
    path('module/<int:module_id>/lesson/add/', views.create_lesson, name='create_lesson'),
    path("module/<int:module_id>/edit/", views.edit_module, name="edit_module"),
    path("module/<int:module_id>/delete/", views.delete_module, name="delete_module"),
    path("lesson/<int:lesson_id>/edit/", views.edit_lesson, name="edit_lesson"),
    path("lesson/<int:lesson_id>/delete/", views.delete_lesson, name="delete_lesson"),
    path('lessons/<int:lesson_id>/complete/', views.CompleteLessonView.as_view(), name='complete_lesson'),
    path('course/<int:course_id>/certificate/', views.generate_certificate, name="generate_certificate"),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
