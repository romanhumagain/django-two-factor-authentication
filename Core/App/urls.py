from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register_user'),
    path('', views.login_view, name='login'),
    path('otp/<slug:slug>/', views.otp_verification, name='otp_verification'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout_user'),
    path('otp-resend/<slug:slug>/', views.otp_verification_resend, name='otp_verification_resend'),
]
