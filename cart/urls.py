
from django.urls import path
from . import views

app_name = 'cart_app'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/', views.cart_remove, name='cart_remove'),
    path('update/', views.cart_update, name='cart_update'),

]