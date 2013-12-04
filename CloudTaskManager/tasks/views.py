from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task
from tasks.forms import TaskForm, ListForm
from django.contrib.auth.decorators import login_required


def user_can_write(user, tasklist):
    if tasklist in user.owned.all():
        return True
    elif tasklist in user.shared.all():
        return True
    elif tasklist in user.readonly.all():
        return False
    else:
        raise Http404


@login_required
def index(request):
    user = request.user.user
    context = {'name': user.get_username(),
               'owned': user.owned.all().order_by('title'),
               'shared': user.shared.all().order_by('title'),
               'readonly': user.readonly.all().order_by('title')}
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
    return render(request, 'tasks/details.html', context)


@login_required
def add_task(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    if not user_can_write(request.user.user, tasklist):
        return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': list_id}))
    if request.method == 'POST':
        task = Task(tasklist=tasklist)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': list_id}))
    else:
        task = Task(tasklist=tasklist)
        form = TaskForm(instance=task)
    context = {'name': request.user.get_username(),
               'tasklist': tasklist,
               'new': True,
               'form': form}
    return render(request, 'tasks/task.html', context)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    list_id = task.tasklist.id
    if not user_can_write(request.user.user, task.tasklist):
        return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': list_id}))
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': list_id}))
    else:
        form = TaskForm(instance=task)
    context = {'name': request.user.get_username(),
               'tasklist': task.tasklist,
               'new': False,
               'form': form}
    return render(request, 'tasks/task.html', context)


@login_required
def add_list(request):
    if request.method == 'POST':
        tasklist = TaskList()
        form = ListForm(request.POST, instance=tasklist)
        if form.is_valid():
            form.save()
            user = request.user.user
            user.owned.add(tasklist)
            return HttpResponseRedirect(reverse('tasks:index'))
    else:
        form = ListForm()
    context = {'name': request.user.get_username(),
               'new': True,
               'form': form}
    return render(request, 'tasks/list.html', context)


def edit_list(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    if not user_can_write(request.user.user, tasklist):
        return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': list_id}))
    if request.method == 'POST':
        form = ListForm(request.POST, instance=tasklist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tasks:index'))
    else:
        form = ListForm(instance=tasklist)
    context = {'name': request.user.get_username(),
               'new': False,
               'form': form}
    return render(request, 'tasks/list.html', context)


@login_required
def check_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    id = task.tasklist.id
    if not user_can_write(request.user.user, task.tasklist):
        if not task.tasklist.readonly_can_check:
            return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': id}))
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': id}))


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
        return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': id}))
    task.delete()
    return HttpResponseRedirect(reverse('tasks:details', kwargs={'list_id': id}))
