"""DBproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import login, logout, register, info
from music.views import index, playlist, comment

urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^accounts/login/$', login, {'template_name':'login.html'}),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),
    url(r'^accounts/register/$', register),
    url(r'^accounts/info/$', info),

    url(r'^playlist/$', playlist),
    url(r'^comment/$', comment),
]
