from django.urls import path
from . import views

app_name = 'payment_app'
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    path('complete-order/', views.complete_order, name='complete-order'),
    

]
