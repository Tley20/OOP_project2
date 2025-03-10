from django.urls import path
from . import views
from .views import login_view
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('register', views.register_choice, name='register'),
    path("register/student/", views.register_student, name="register_student"),
    path("register/teacher/", views.register_teacher, name="register_instructor"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

]
