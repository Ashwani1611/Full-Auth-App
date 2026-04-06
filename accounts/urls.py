from django.urls import path
from .views import RegisterView , ProfileView , ChangePasswordView , ForgotPasswordView , ResetPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    # login
    path('login/',TokenObtainPairView.as_view(),name='login'),
    # path('login/',CustomTokenView.as_view(),name='login'),

    # Refresh Token
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    path('profile/',ProfileView.as_view(),name='profile'),

    #Change password
    path('change_password/',ChangePasswordView.as_view(),name='change_password'),

    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),

    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),



]