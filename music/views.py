from django.shortcuts import render
from django.db import models

# Create your views here.

def index(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'index.html', locals())
