from django import forms
from django.forms.extras.widgets import SelectDateWidget
from tasks.models import User, TITLE_LENGTH, DESCR_LENGTH, CATEG_LENGTH

# Enumeration of types of sharing
SHARE_WRITE = 'wr'
SHARE_READ = 'ro'

USER_LENGTH = 25
PASS_LENGTH = 30


class ListForm(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=TITLE_LENGTH)
    description = forms.CharField(label='Description',
                                  max_length=DESCR_LENGTH,
                                  widget=forms.Textarea,
                                  required=False)
    category = forms.CharField(label='Category',
                               max_length=CATEG_LENGTH, required=False)


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


class ShareForm(forms.Form):
    username = forms.CharField(label='User', max_length=USER_LENGTH)
    share_mode = forms.ChoiceField(label='User can edit?',
                                   choices=((SHARE_WRITE, 'Yes'),
                                            (SHARE_READ, 'No')))
