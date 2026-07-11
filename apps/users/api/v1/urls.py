from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from .views import (RegisterView, LoginView, ProfileView, DeleteAccountView, 
                    LogoutView, ChangePasswordView)

app_name = 'api/v1'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('account/', DeleteAccountView.as_view(), name='delete_account'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(),
         name="change-password"),
]