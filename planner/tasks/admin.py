from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'workspace', 'owner')
    list_filter = ('status', 'workspace')
    search_fields = ('title', 'content')

