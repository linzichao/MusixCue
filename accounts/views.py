from django.shortcuts import render
from django.contrib.auth.views import login, logout
import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html')
