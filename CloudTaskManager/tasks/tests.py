from django.test import TestCase
from tasks.models import TaskList, Task


class TaskListMethodTests(TestCase):
    TASKLIST_TITLE = 'TEST___TESTTASKLIST'
    TASKLIST_DESCR = 'A TEST TASK LIST'
    TASKLIST_CATEG = 'TESTING'

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
