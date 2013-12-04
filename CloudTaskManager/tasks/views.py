from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task, User
from tasks.forms import TaskForm, ListForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser


def user_can_write(user, tasklist):
    if tasklist in user.owned.all():
        return True
    elif tasklist in user.shared.all():
        return True
    elif tasklist in user.readonly.all():
        return False
    else:
        raise Http404


def register(request):
    passwords_match = True
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']
            passwords_match = password == confirm
            if passwords_match:
                authuser = AuthUser.objects.create_user(username,
                                                        email,
                                                        password)
                user = User(authuser=authuser)
                user.save()
                return HttpResponseRedirect(reverse('tasks:index'))
    else:
        form = UserForm()
    context = {'form': form, 'error': passwords_match}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/register.html', context)


@login_required
def index(request):
    user = request.user.user
    context = {'name': user.get_username(),
               'owned': user.owned.all().order_by('title'),
               'shared': user.shared.all().order_by('title'),
               'readonly': user.readonly.all().order_by('title')}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/index.html', context)


@login_required
def details(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    can_edit = user_can_write(request.user.user, tasklist)
    tasks_list = tasklist.task_set.all().order_by('due_date')
    context = {'name': request.user.get_username(),
               'can_edit': can_edit,
               'tasklist': tasklist,
               'tasks_list': tasks_list,
               'list_id': list_id}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/details.html', context)


@login_required
def add_list(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            readonly = form.cleaned_data['readonly']
            tasklist = TaskList(title=title,
                                description=description,
                                category=category,
                                readonly_can_check=readonly)
            tasklist.save()
            user = request.user.user
            user.owned.add(tasklist)
            return HttpResponseRedirect(reverse('tasks:index'))
    else:
        form = ListForm()
    context = {'name': request.user.get_username(),
               'new': True,
               'form': form}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/list.html', context)


@login_required
def edit_list(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    if not user_can_write(request.user.user, tasklist):
        return HttpResponseRedirect(reverse('tasks:details',
                                    kwargs={'list_id': list_id}))
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            tasklist.title = form.cleaned_data['title']
            tasklist.description = form.cleaned_data['description']
            tasklist.category = form.cleaned_data['category']
            tasklist.readonly_can_check = form.cleaned_data['readonly']
            tasklist.save()
            return HttpResponseRedirect(reverse('tasks:details',
                                        kwargs={'list_id': tasklist.id}))
    else:
        form = ListForm()
    context = {'name': request.user.get_username(),
               'new': False,
               'form': form}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/list.html', context)


@login_required
def add_task(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    if not user_can_write(request.user.user, tasklist):
        return HttpResponseRedirect(reverse('tasks:details',
                                    kwargs={'list_id': list_id}))
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task(tasklist=tasklist,
                        title=form.cleaned_data['title'],
                        description=form.cleaned_data['description'],
                        category=form.cleaned_data['category'],
                        due_date=form.cleaned_data['due_date'])
            task.save()
            return HttpResponseRedirect(reverse('tasks:details',
                                        kwargs={'list_id': list_id}))
    else:
        form = TaskForm()
    context = {'name': request.user.get_username(),
               'tasklist': tasklist,
               'new': True,
               'form': form}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/task.html', context)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    list_id = task.tasklist.id
    if not user_can_write(request.user.user, task.tasklist):
        return HttpResponseRedirect(reverse('tasks:details',
                                    kwargs={'list_id': list_id}))
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.category = form.cleaned_data['category']
            task.due_date = form.cleaned_data['due_date']
            task.save()
            return HttpResponseRedirect(reverse('tasks:details',
                                        kwargs={'list_id': list_id}))
    else:
        form = TaskForm()
    context = {'name': request.user.get_username(),
               'tasklist': task.tasklist,
               'new': False,
               'form': form}
    context['logged_in'] = request.user and request.user.is_authenticated()
    return render(request, 'tasks/task.html', context)


@login_required
def check_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    id = task.tasklist.id
    if not user_can_write(request.user.user, task.tasklist):
        if not task.tasklist.readonly_can_check:
            return HttpResponseRedirect(reverse('tasks:details',
                                        kwargs={'list_id': id}))
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect(reverse('tasks:details',
                                kwargs={'list_id': id}))


@login_required
def delete_list(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    user = request.user.user
    if not user_can_write(user, tasklist):
        return HttpResponseRedirect(reverse('tasks:index'))
    if tasklist in user.owned.all():
        tasklist.delete()
    elif tasklist in user.shared.all():
        user.shared.remove(tasklist)
    elif tasklist in user.readonly.all():
        user.readonly.remove(tasklist)
    return HttpResponseRedirect(reverse('tasks:index'))


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    id = task.tasklist.id
    if not user_can_write(request.user.user, task.tasklist):
        return HttpResponseRedirect(reverse('tasks:details',
                                    kwargs={'list_id': id}))
    task.delete()
    return HttpResponseRedirect(reverse('tasks:details',
                                kwargs={'list_id': id}))
