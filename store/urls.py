from django.urls import path
from . import views

app_name = 'store_app'

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:product_slug>', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>', views.category_list, name='category_list'),
    
]