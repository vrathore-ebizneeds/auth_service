from collections import UserList
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from drf_spectacular.views import (SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView)

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
 
    path('password-reset/'       , views.PasswordResetRequestAPI.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmAPI.as_view(), name='password_reset_confirm'),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger_ui"),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name="schema"), name="redoc")
]