from django.contrib import admin
from django.urls import path
from .views import *  # Import the view
from django.conf.urls.static import static

urlpatterns = [
    path('', admin.site.urls),
]