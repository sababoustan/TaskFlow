from django.urls import include, path

app_name = "users"

urlpatterns = [
    path("auth/", include("apps.users.api.v1.urls")),
]
