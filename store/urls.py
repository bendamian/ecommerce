from django.urls import path
from . import views

app_name = 'store_app'

urlpatterns = [
    path('', views.store, name='store'),

]