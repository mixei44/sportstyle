from django.urls import path
from django.contrib.auth.views import LogoutView
from user.views import (validate_email_view, validate_passwords_view, validate_accept_policy_view, 
                        SignupView, LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, email_verify_view)

urlpatterns = [
    path('validate_email/', validate_email_view, name='validate_email'),
    path('validate_passwords/', validate_passwords_view, name='validate_passwords'),
    path('validate_policy/', validate_accept_policy_view, name='validate_policy'),
    
    path('signup/', SignupView.as_view(), name='signup'),
    path('email_verify/<uidb64>/<token>/', email_verify_view, name='email_verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_change/', PasswordChangeView.as_view(), name="password_change"),
]
