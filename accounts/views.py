from django.shortcuts import render
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse


import datetime

# Create your views here.

class profileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', locals())


def info(request):

    if request.user.is_authenticated:
        if request.method == 'GET': #info UI
            form = profileForm(initial={'email': request.user.email, \
                                        'first_name': request.user.first_name, 'last_name': request.user.last_name})
            return render(request, 'info.html', locals())

        elif request.method == 'POST': #update info
            form = profileForm(data=request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect("/accounts/info")
    else:
        return HttpResponseRedirect("/")

def is_loggin(request):

    if request.user.is_authenticated:
        return HttpResponse('')
    else:
        return HttpResponse('Unauthorized', status=401)
