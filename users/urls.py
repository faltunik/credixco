from django.urls import path
from . import views
from .views import MyTokenObtainPairView


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', views.CustomUserCreate.as_view(), name='register'),
    path('profile', views.get_profile, name='profile'),
    path('mystudent', views.create_student, name='create-student'),
    path('mystudentlist', views.get_student, name='list-student'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
    #      name='password_reset_confirm'),
]