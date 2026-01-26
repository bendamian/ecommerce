from django.urls import path
from . import views

app_name = 'payment_app'
urlpatterns = [
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    

]
