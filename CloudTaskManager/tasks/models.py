from django.db import models
import datetime
from django.utils import timezone

MODELS_TITLELENGTH = 50
MODELS_DESCRLENGTH = 300
MODELS_CATEGLENGTH = 20
MODELS_LATESTR     = 'late'
MODELS_SOONSTR     = 'due soon'
MODELS_TOMORROWSTR = 'due tomorrow'

# class User(models.Model):

class TaskList(models.Model):
    title = models.CharField(max_length=MODELS_TITLELENGTH)
    description = models.CharField(max_length=MODELS_DESCRLENGTH)
    category = models.CharField(max_length=MODELS_CATEGLENGTH)
    # users = models.ManyToManyfield(User)
    def __str__(self):
        return '{0}: {1}'.format(self.title, self.description)

class Task(models.Model):
    task_list = models.ForeignKey(TaskList)
    title = models.CharField(max_length=MODELS_TITLELENGTH)
    #order = models.IntegerField(default=0) # TODO: Add
    description = models.CharField(max_length=MODELS_DESCRLENGTH)
    category = models.CharField(max_length=MODELS_CATEGLENGTH)
    due_date = models.DateTimeField('Due')
    is_completed = models.BooleanField('Completed?', default=False)

    def is_late(self):
        return self.due_date < timezone.now()
    def is_due_this_week(self):
        return not self.is_late() and self.due_date <= timezone.now() + datetime.timedelta(days=7)
    def is_due_tomorrow(self):
        return not self.is_late() and self.due_date <= timezone.now() + datetime.timedelta(days=1)
    def status(self):
        if self.is_late():
            return MODELS_LATESTR
        if self.is_due_this_week():
            return MODELS_SOONSTR
        if self.is_due_tomorrow():
            return MODELS_TOMORROWSTR
    status.admin_order_field = 'due_date'
    status.short_description = 'Status'

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.description)

