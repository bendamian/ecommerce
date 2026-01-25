from django.urls import include, path, reverse_lazy
from . import views
# Import Django's built-in authentication views for password reset
from django.contrib.auth import views as auth_views

app_name = 'account_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('email-verify/<str:uidb64>/<str:token>/',
         views.email_verification, name='email-verify'),
    path('email-verify-failed/', views.email_verification_failed,
         name='email-verify-failed'),
    path('email-verify-success/', views.email_verification_success,
         name='email-verify-success'),
    path('email-verify-sent/', views.email_verification_sent,
         name='email-verify-sent'),
    path('my-login/', views.my_login, name='my-login'),
    path('my-logout/', views.my_logout, name='my-logout'),


    # profile management
    path('profile-management/', views.profile_management,
         name='profile-management'),
    path('delete-account/', views.delete_account, name='delete-account'),
    path('dashboard/', views.dashboard, name='dashboard'),


    # Include password reset URLs from urls_password.py
    path('', include('account.urls_password')),

   

]
