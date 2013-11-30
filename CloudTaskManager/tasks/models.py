from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser

TITLE_LENGTH = 50
DESCR_LENGTH = 300
CATEG_LENGTH = 20
LATE_STR = 'late'
SOON_STR = 'due soon'
TOMORROW_STR = 'due tomorrow'


class TaskList(models.Model):
    title = models.CharField(max_length=TITLE_LENGTH)
    category = models.CharField(max_length=CATEG_LENGTH)
    description = models.CharField(max_length=DESCR_LENGTH,
                                   null=True,
                                   blank=True)

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.description)


class Task(models.Model):
    tasklist = models.ForeignKey(TaskList)
    title = models.CharField(max_length=TITLE_LENGTH)
    #order = models.IntegerField(default=0) # TODO: Add
    category = models.CharField(max_length=CATEG_LENGTH)
    due_date = models.DateTimeField('Due', null=True, blank=True)
    is_completed = models.BooleanField('Completed?', default=False)
    description = models.CharField(max_length=DESCR_LENGTH,
                                   null=True,
                                   blank=True)

    def is_late(self):
        return self.due_date < timezone.now()

    def is_due_this_week(self):
        if self.is_late():
            return False
        return self.due_date <= timezone.now() + datetime.timedelta(days=7)

    def is_due_tomorrow(self):
        if self.is_late():
            return False
        return self.due_date <= timezone.now() + datetime.timedelta(days=1)

    def status(self):
        if self.is_late():
            return LATE_STR
        if self.is_due_tomorrow():
            return TOMORROW_STR
        if self.is_due_this_week():
            return SOON_STR
    status.admin_order_field = 'due_date'
    status.short_description = 'Status'

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.description)


class User(models.Model):
    authuser = models.OneToOneField(AuthUser)
    owned = models.ManyToManyField(TaskList, related_name='xw+')
    shared = models.ManyToManyField(TaskList, related_name='rw+')
    readonly = models.ManyToManyField(TaskList, related_name='ro+')

    def get_username(self):
        return self.authuser.get_username()

    def get_firstname(self):
        return self.authuser.first_name

    def get_name(self):
        return self.authuser.get_full_name()
