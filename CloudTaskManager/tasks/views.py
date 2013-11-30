from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task
from tasks.forms import TaskForm, ListForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user = request.user.user
    context = {'owned': user.owned.all().order_by('title'),
               'shared': user.shared.all().order_by('title'),
               'shared': user.shared.all().order_by('title')}
    return render(request, 'tasks/index.html', context)


@login_required
def details(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    tasks_list = tasklist.task_set.all().order_by('due_date')
    context = {'tasklist': tasklist,
               'tasks_list': tasks_list,
               'list_id': list_id}
    return render(request, 'tasks/details.html', context)


@login_required
def addTask(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    if request.method == 'POST':
        #form = TaskForm(request.POST)
        task = Task(tasklist=tasklist)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            #task = Task(tasklist=tasklist,
                        #title=form.cleaned_data['title'],
                        #description=form.cleaned_data['description'],
                        #due_date=form.cleaned_data['due_date'],
                        #category=form.cleaned_data['category'])
            #task.save()
            return HttpResponseRedirect('/tasklists/{0}/'.format(list_id))
    else:
        task = Task(tasklist=tasklist)
        form = TaskForm(instance=task)
    return render(request, 'tasks/addTask.html', {'form': form})


@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            #task.title = form.cleaned_data['title']
            #task.description = form.cleaned_data['description']
            #task.category = form.cleaned_data['category']
            #task.due_date = form.cleaned_data['due_date']
            #task.save()
            list_id = task.tasklist.id
            return HttpResponseRedirect('/tasklists/{0}/'.format(list_id))
    else:
        form = TaskForm(instance=task)
    return render(request,
                  'tasks/edit.html',
                  {'tasklist': task.tasklist, 'form': form})


@login_required
def addList(request):
    if request.method == 'POST':
        tasklist = TaskList()
        form = ListForm(request.POST, instance=tasklist)
        if form.is_valid():
            form.save()
            user = request.user.user
            user.owned.add(tasklist)
            return HttpResponseRedirect('/tasklists/')
    else:
        form = ListForm()
    return render(request, 'tasks/addList.html', {'form': form})


@login_required
def save(request, list_id):
    return HttpResponse("Saved! (not actually though)")


@login_required
def check_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.is_completed = not task.is_completed
    id = task.tasklist.id
    task.save()
    return HttpResponseRedirect('/tasklists/{0}/'.format(id))


@login_required
def delete_list(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    tasklist.delete()
    return HttpResponseRedirect('/tasklists/')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    id = task.tasklist.id
    task.delete()
    return HttpResponseRedirect('/tasklists/{0}/'.format(id))
