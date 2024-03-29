from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from ahms.users import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("home", views.home, name="home"),

    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("ahms.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("appointment/", include("ahms.appointments.urls", namespace="appointments")),
    path('accounts/signup/doctor', views.DoctorSignUpView.as_view(), name='doctor_signup'),
    path('accounts/signup/nurse/', views.NurseSignUpView.as_view(), name='nurse_signup'),
    path('accounts/signup/patient/', views.PatientSignUpView.as_view(), name='patient_signup'),
    path('accounts/signup/patient/patient-profile-update',
         views.PatientProfileUpdate.as_view(),
         name='patient_profile_update'),
    # path('accounts/patient/patient-details',
    #      views.PatientDetail.as_view(),
    #      name="patient_detail"),
    path('accounts/signup/patient/nurse-profile-update',
         views.NurseProfileUpdate.as_view(),
         name='patient_profile_update'),
    path('accounts/signup/patient/doctor-profile-update',
         views.DoctorProfileUpdate.as_view(),
         name='patient_profile_update'),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
