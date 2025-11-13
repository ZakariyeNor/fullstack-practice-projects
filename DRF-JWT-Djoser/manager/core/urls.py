from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view
schema_view = get_schema_view(
    openapi.Info(
        title="API Docs.",
        default_version="v1",
        description="Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")), 
    
    path("auth/password/reset/", PasswordResetView.as_view(), name='password_reset'),
    path(
        "auth/password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),

    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"
    ),
    
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
