from django.contrib import admin
from music.models import *
from django.apps import apps

for model in apps.get_app_config('music').models.values():
    admin.site.register(model)

