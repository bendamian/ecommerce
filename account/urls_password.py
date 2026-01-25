# account/urls_password.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
 
    # Password Reset URLs
    # Using Django's built-in auth views with custom templates


    # 1-submit email form
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='account/password/password_reset.html',
            email_template_name='account/password/password_reset_email.html',
            subject_template_name='account/password/password_reset_subject.txt',
            success_url=reverse_lazy('account_app:reset_password_done'),
        ),
        name='reset_password',
    ),
    # 2-password reset email was sent
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password/password_reset_sent.html'),
         name='reset_password_done'),
    # 3-password reset Link
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password/password_reset_form.html',
             success_url=reverse_lazy('account_app:password_reset_complete'),),
         name='password_reset_confirm'),
    # 4-password reset complete success message
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password/password_reset_complete.html'),
         name='password_reset_complete'),






]    # Password Reset URLs
    # Using Django's built-in auth views with custom templates