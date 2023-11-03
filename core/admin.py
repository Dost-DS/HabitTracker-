from django.contrib import admin

# Register your models here.
from .models import Habit, CompletedTask

admin.site.register(Habit)
admin.site.register(CompletedTask)