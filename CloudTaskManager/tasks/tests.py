from django.test import TestCase
from tasks.models import TaskList, Task
from django.utils import timezone
import datetime

class TaskListMethodTests(TestCase):
    TASKLIST_TITLE = 'TEST___TESTTASKLIST'
    TASKLIST_DESCR = 'A TEST TASK LIST'
    TASKLIST_CATEG = 'TESTING'
    TASK_TITLE = 'TEST_TASK'
    TASK_DESCR = 'TEST_DESCR'
    TASK_CATEGORY = 'TEST_TASKS'
    TASK_DUEDATE = datetime.datetime(2003, 8, 4, 7, 17)
	
    def test_create_tasklist(self):
        """
        Tests that task lists can be added to the database.
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        retreived_tasklist = None
        try:
            tasklist.save()
            retreived_tasklist = TaskList.objects.get(title=self.TASKLIST_TITLE)
            self.assertEqual(tasklist, retreived_tasklist)
            retreived_tasklist.delete()
            preserved_retreived = TaskList.objects.filter(title=self.TASKLIST_TITLE)
            self.assertTrue(not preserved_retreived)
        except:
            self.assertTrue(False)
	
    def test_create_task(self):
        """
        Tests that tasks can be added to task lists.
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        tasklist.save()
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=self.TASK_DUEDATE,
                is_completed=False)
        retrieved_task = None
        try:
            task.save()
            retrieved_task = Task.objects.get(title=self.TASK_TITLE)
            self.assertEqual(task, retrieved_task)
            retrieved_task.delete()
        except:
            self.assertTrue(False)

    def test_is_late_true(self):
        """
        Tests that tasks can be late
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=self.TASK_DUEDATE,
                is_completed=False)
        self.assertTrue(task.is_late())
		
    def test_is_late_false(self):
        """
        Tests that tasks can be late
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() + datetime.timedelta(days=2) 
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertFalse(task.is_late())

    def test_is_due_this_week_false(self):
        """
        Tests that we return false if task is not due this week
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=self.TASK_DUEDATE,
                is_completed=False)
        self.assertFalse(task.is_due_this_week())

    def test_is_due_this_week_true(self):
        """
        Tests that if something is due this week, we display that it is
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date=timezone.now() - datetime.timedelta(days=1)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertFalse(task.is_due_this_week())

    def test_is_due_tomorrow_false(self):
        """
        Tests that if something is not due tomorrow, we don't display that it is due tomorrow
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=self.TASK_DUEDATE,
                is_completed=False)
        self.assertFalse(task.is_due_tomorrow())

    def test_is_due_tomorrow_true(self):
        """
        Tests that if something is not due tomorrow, we don't display that it is due tomorrow
        """
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date=timezone.now() + datetime.timedelta(days=1)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertTrue(task.is_due_tomorrow())

    def test_status_none(self):
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date=timezone.now() + datetime.timedelta(days=15)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertEqual(task.status(), None)

    def test_status_late(self):
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date=timezone.now() - datetime.timedelta(days=15)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertEqual(task.status(), 'late')

    def test_status_is_due_this_week(self):
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date=timezone.now() + datetime.timedelta(days=4)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertEqual(task.status(), 'due soon')

    def test_status_is_due_tomorrow(self):
        tasklist = TaskList(
                title=self.TASKLIST_TITLE,
                description=self.TASKLIST_DESCR,
                category=self.TASKLIST_CATEG)
        new_due_date=timezone.now() + datetime.timedelta(days=1)
        task = Task(task_list=tasklist,
                title=self.TASK_TITLE,
                description=self.TASK_DESCR,
                category=self.TASK_CATEGORY,
                due_date=new_due_date,
                is_completed=False)
        self.assertEqual(task.status(), 'due tomorrow')
