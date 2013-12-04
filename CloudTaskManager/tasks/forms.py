from django import forms
from django.forms.extras.widgets import SelectDateWidget
from tasks.models import TITLE_LENGTH, DESCR_LENGTH, CATEG_LENGTH

USER_LENGTH = 25
PASS_LENGTH = 30


#class TaskForm(ModelForm):
    #class Meta:
        #model = Task
        #fields = ['title', 'description', 'due_date', 'tasklist']


#class ListForm(ModelForm):
    #class Meta:
        #model = TaskList
        #fields = ['title', 'description', 'category', 'readonly_can_check']


class ListForm(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=TITLE_LENGTH)
    description = forms.CharField(label='Description',
                                  max_length=DESCR_LENGTH,
                                  widget=forms.Textarea,
                                  required=False)
    category = forms.CharField(label='Category',
                               max_length=CATEG_LENGTH, required=False)
    readonly = forms.BooleanField(label='Shared can edit?', required=False)


class TaskForm(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=TITLE_LENGTH)
    description = forms.CharField(label='Description',
                                  max_length=DESCR_LENGTH,
                                  widget=forms.Textarea,
                                  required=False)
    category = forms.CharField(label='Category',
                               max_length=CATEG_LENGTH, required=False)
    due_date = forms.DateField(label='Date due',
                               required=False,
                               widget=SelectDateWidget)


class UserForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=USER_LENGTH)
    email = forms.CharField(label='Email Address',
                            max_length=USER_LENGTH,
                            widget=forms.EmailInput)
    password = forms.CharField(label='Password',
                               max_length=PASS_LENGTH,
                               widget=forms.PasswordInput)
    confirm = forms.CharField(label='Confirm password',
                              max_length=PASS_LENGTH,
                              widget=forms.PasswordInput)
