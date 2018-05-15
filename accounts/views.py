from django.shortcuts import render
from django.contrib.auth.views import login, logout

# Create your views here.

def index(request):
    return render(request, 'index.html')
