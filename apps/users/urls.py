from django.urls import path, include


app_name = 'users'

urlpatterns = [
    path('auth/', include('apps.users.api.v1.urls')),
]