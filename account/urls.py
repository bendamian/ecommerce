from django.urls import path
from . import views

app_name = 'account_app'

urlpatterns = [
 path('register/', views.register, name='register'),
 path('email-verify/', views.email_verification, name='email-verify'),
 path('email-verify-failed/', views.email_verification_failed, name='email-verify-failed'),
 path('email-verify-success/', views.email_verification_success, name='email-verify-success'),
 path('email-verify-sent/', views.email_verification_sent, name='email-verify-sent'),
    
]
