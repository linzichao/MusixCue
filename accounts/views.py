from django.shortcuts import render
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
import datetime

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())
