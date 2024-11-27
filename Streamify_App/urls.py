from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from .views import * # Import your views file
from . import views 


urlpatterns = [
   path('', views.index, name='index'),  # Home page
    path('home/', views.index, name='home'),  # Redirect to home if needed
    path('sign_in/', views.sign_in, name='sign_in'),  # Combined sign-in and sign-up handling
    path('movie-recommendation/', views.movie_recommendation, name='movie_recommendation'),  # Movie recommendation
    path('analysis/', views.analysis, name='analysis'),  # Movie recommendation


]
