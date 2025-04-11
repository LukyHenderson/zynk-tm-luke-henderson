from django.contrib import admin
from .models import Task

admin.site.register(Task) # adds task models to admin site
