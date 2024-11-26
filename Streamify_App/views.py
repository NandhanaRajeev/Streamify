import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views import View

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')
