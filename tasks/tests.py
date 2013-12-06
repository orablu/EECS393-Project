from django.test import TestCase
from tasks.models import TaskList, Task, User
from django.contrib.auth.models import User as AuthUser
import tasks.forms
import tasks.urls
import tasks.views
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login


class TaskListMethodTests(TestCase):
    TASKLIST_TITLE = 'TEST___TESTTASKLIST'
    TASKLIST_DESCR = 'A TEST TASK LIST'
    TASKLIST_CATEG = 'TESTING'
    TASK_TITLE = 'TEST_TASK'
    TASK_DESCR = 'TEST_DESCR'
    TASK_CATEGORY = 'TEST_TASKS'
    TASK_DUEDATE = datetime.datetime(2003, 8, 4, 7, 17)

    AuthUser.objects.create_user('test',
                                 'test@test.com',
                                 'test')
    authuser = authenticate(username='test',
                            password='test')
    def test_string_function(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        self.assertEqual(tasklist.__str__(), 'TEST___TESTTASKLIST: A TEST TASK LIST')

    def test_string_function_task(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        task = Task(tasklist=tasklist,
                    title=self.TASK_TITLE,
                    description=self.TASK_DESCR,
                    category=self.TASK_CATEGORY,
                    due_date=self.TASK_DUEDATE,
                    is_completed=False)
        self.assertEqual(task.__str__(), 'TEST_TASK: TEST_DESCR')

    def test_get_username_and_names(self):
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        self.assertEqual(user.get_username(), "test")
        self.assertEqual(user.get_firstname(), "")
        self.assertEqual(user.get_name(), "")

    def test_create_tasklist(self):
        """
        Tests that task lists can be added to the database.
        """
        tasklist = TaskList(title=self.TASKLIST_TITLE,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        tasklist.save()
        task = Task(tasklist=tasklist,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        task = Task(tasklist=tasklist,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() + datetime.timedelta(days=2)
        task = Task(tasklist=tasklist,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        task = Task(tasklist=tasklist,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() - datetime.timedelta(days=1)
        task = Task(tasklist=tasklist,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        task = Task(tasklist=tasklist,
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
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() + datetime.timedelta(days=1)
        task = Task(tasklist=tasklist,
                    title=self.TASK_TITLE,
                    description=self.TASK_DESCR,
                    category=self.TASK_CATEGORY,
                    due_date=new_due_date,
                    is_completed=False)
        self.assertTrue(task.is_due_tomorrow())

    def test_status_none(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() + datetime.timedelta(days=15)
        task = Task(tasklist=tasklist,
                    title=self.TASK_TITLE,
                    description=self.TASK_DESCR,
                    category=self.TASK_CATEGORY,
                    due_date=new_due_date,
                    is_completed=False)
        self.assertEqual(task.status(), 'ok')

    def test_status_late(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() - datetime.timedelta(days=15)
        task = Task(tasklist=tasklist,
                    title=self.TASK_TITLE,
                    description=self.TASK_DESCR,
                    category=self.TASK_CATEGORY,
                    due_date=new_due_date,
                    is_completed=False)
        self.assertEqual(task.status(), 'late')

    def test_status_is_due_this_week(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() + datetime.timedelta(days=4)
        task = Task(tasklist=tasklist,
                    title=self.TASK_TITLE,
                    description=self.TASK_DESCR,
                    category=self.TASK_CATEGORY,
                    due_date=new_due_date,
                    is_completed=False)
        self.assertEqual(task.status(), 'due soon')

    def test_status_is_due_tomorrow(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        new_due_date = timezone.now() + datetime.timedelta(days=1)
        task = Task(tasklist=tasklist,
                    title=self.TASK_TITLE,
                    description=self.TASK_DESCR,
                    category=self.TASK_CATEGORY,
                    due_date=new_due_date,
                    is_completed=False)
        self.assertEqual(task.status(), 'due tomorrow')

    def test_user_can_write_owned(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        user.owned.add(tasklist)
        self.assertTrue(tasks.views.user_can_write(user,tasklist))

    def test_user_can_write_shared(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        authuser.user.shared.add(tasklist)
        self.assertTrue(tasks.views.user_can_write(user,tasklist))

    def test_user_cannot_write_readonly(self):
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        authuser.user.readonly.add(tasklist)
        self.assertFalse(tasks.views.user_can_write(user,tasklist))

    def test_users_should_be_logged_in(self):
        request = self.client.get('/login/', follow=True)
        self.assertTemplateUsed(request, 'tasks/login.html')
        self.assertEqual(request.status_code, 200)
        request = self.client.post('/url/to/view', follow=True)
        self.assertTemplateUsed(request, 'tasks/login.html')

    def test_user_login_again(self):
        request = self.client.get('/register/', follow=True)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'tasks/register.html')
        response = self.client.post('/register/', follow=True)
        self.assertTemplateUsed(response, 'tasks/register.html')
        self.assertEqual(response.status_code, 200)
       
    def something(self):
        self.client.login(username='user', password='test')  # defined in fixture
        response = self.client.get('/index/', follow=True)
        self.assertRedirects(request, '/login/')

    def test_add_list(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('tasks/add.html')

    def test_details(self):
        self.client.login(username='test', password='test')
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        user.owned.add(tasklist)
        response = self.client.get('/1/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('tasks/details.html')
        
    def test_cannot_edit_list(self):
        self.client.login(username='test', password='test')
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        user.readonly.add(tasklist)
        response = self.client.get('/1/edit/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('tasks/edit.html')

    def test_can_edit_list(self):
        self.client.login(username='test', password='test')
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        user.shared.add(tasklist)
        response = self.client.get('/1/edit/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_shared_lists(self): 
        self.client.login(username='test', password='test')
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        user.owned.add(tasklist)
        response = self.client.get('/1/share/', follow=True)
        request = self.client.post('/1/share/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_tasklist(self):
        self.client.login(username='test', password='test')
        response = self.client.get('/add/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_task(self):
        self.client.login(username='test', password='test')
        tasklist = TaskList(title=self.TASKLIST_TITLE,
                            description=self.TASKLIST_DESCR,
                            category=self.TASKLIST_CATEG)
        authuser = authenticate(username='test',
                                password='test')
        user = User(authuser=authuser)
        tasklist.save()
        user.save()
        response = self.client.get('/1/add/', follow=True)
        self.assertTemplateUsed("tasks/add.html") 
