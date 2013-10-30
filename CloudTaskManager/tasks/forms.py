from django.forms import ModelForm
from tasks.models import Task, TaskList

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['title', 'description', 'due_date']

class ListForm(ModelForm):
	class Meta:
		model = TaskList
		fields = ['title', 'description', 'category']