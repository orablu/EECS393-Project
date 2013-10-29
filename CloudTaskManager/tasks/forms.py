from django import forms

class TaskForm(forms.Form):
	title = forms.CharField()
	description = forms.CharField(required=False)
	due_date = forms.DateTimeField(required=False)