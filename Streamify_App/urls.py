from django.contrib import admin
from django.urls import path
from .views import index,contact  # Import your views file

urlpatterns = [
    path('', index, name='index'),  # Add this line if missing
    path('contact', contact, name='contact'), 
]
