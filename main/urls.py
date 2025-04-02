from django.urls import path
from . import views
from .views import login_view
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="SkillHorizon API",
        default_version='v1',
        description="Документация API",
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'certificates', views.CertificateViewSet)
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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
