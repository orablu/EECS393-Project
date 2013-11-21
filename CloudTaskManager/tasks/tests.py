from django.test import TestCase
from tasks.models import TaskList, Task
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

    def test_is_late(self):
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
	