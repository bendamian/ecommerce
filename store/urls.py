from django.urls import path
from . import views

app_name = 'store_app'

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    


]