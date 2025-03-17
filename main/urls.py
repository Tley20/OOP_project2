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
    path("course/<int:pk>/enroll/", views.enroll_course, name="enroll_course"),
    path('courses/', views.course_list, name='course_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
