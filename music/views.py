from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'index.html', locals())

# User's playlist
def playlist(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'playlist.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")

def comment(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'comment.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")
