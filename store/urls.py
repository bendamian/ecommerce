from django.urls import path
from . import views

app_name = 'store_app'

urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail')


]