from django.contrib import admin
from tasks.models import TaskList, Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

class TaskListAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,      {'fields': ['title']}),
            ('Details', {'fields': ['description', 'category'], 'classes': ['collapse']}),
    ]
    inlines = [TaskInline]

admin.site.register(TaskList, TaskListAdmin)
