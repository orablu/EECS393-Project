from django.db import models
import datetime
from django.utils import timezone

TITLELENGTH = 50
DESCRLENGTH = 300
CATEGLENGTH = 20
WEEKINDAYS  = 7

# class User(models.Model):

class TaskList(models.Model):
    title = models.CharField(max_length=TITLELENGTH)
    description = models.CharField(max_length=DESCRLENGTH)
    category = models.CharField(max_length=CATEGLENGTH)
    # users = models.ManyToManyfield(User)
    def __str__(self):
        return '{0}: {1}'.format(self.title, self.description)

class Task(models.Model):
    task_list = models.ForeignKey(TaskList)
    title = models.CharField(max_length=TITLELENGTH)
    description = models.CharField(max_length=DESCRLENGTH)
    category = models.CharField(max_length=CATEGLENGTH)
    due_date = models.DateTimeField('Due')
    is_completed = models.BooleanField('Completed?', default=False)

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.description)

    def is_late(self):
        return self.due_date < timezone.now()

    def is_due_this_week(self):
        return not self.is_late() and self.due_date <= timezone.now() + datetime.timedelta(days=WEEKINDAYS)
