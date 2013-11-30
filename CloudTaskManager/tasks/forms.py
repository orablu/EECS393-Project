from django.forms import ModelForm
#from django import forms
from tasks.models import Task, TaskList
#from tasks.models import TITLE_LENGTH, DESCR_LENGTH, CATEG_LENGTH


#class TaskForm(forms.Form):
    #title = forms.CharField(max_length=TITLE_LENGTH)
    #description = forms.CharField(max_length=DESCR_LENGTH)
    #category = forms.CharField(max_length=CATEG_LENGTH)
    #due_date = forms.DateField()


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'tasklist']


class ListForm(ModelForm):
    class Meta:
        model = TaskList
        fields = ['title', 'description', 'category']
