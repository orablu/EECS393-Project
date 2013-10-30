from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task
from tasks.forms import TaskForm, ListForm


def index(request):
    context = {'task_list_list': TaskList.objects.order_by('title')}
    return render(request, 'tasks/index.html', context)


def details(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    tasks_list = tasklist.task_set.all()
    context = {'tasklist': tasklist,
        'tasks_list': tasks_list,
        'list_id': list_id}
    return render(request, 'tasks/details.html', context)


def addTask(request, list_id):
	tasklist, created = TaskList.objects.get_or_create(pk=list_id)
	if request.method == 'POST':
		task = Task(task_list=tasklist)
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/tasklists/' + list_id + '/')
	else:
		task = Task(task_list=tasklist)
		form = TaskForm(instance=task)
	return render(request, 'tasks/addTask.html', {'form': form,})

def edit(request, task_id):
	task = get_object_or_404(Task, pk=task_id)
	form = TaskForm(instance=task)
	return render(request, 'tasks/edit.html', {'form': form})

def addList(request):
    if request.method == 'POST':
        tasklist = TaskList()
        form = ListForm(request.POST, instance=tasklist)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/tasklists/')
    else:
        form = ListForm()
    return render(request, 'tasks/addList.html', {'form': form})


def save(request, list_id):
    return HttpResponse("Saved! (not actually though)")


def check_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    tasklist = task.task_list
    task.is_completed = not task.is_completed
    return HttpResponseRedirect('/tasklists/{0}/'.format(tasklist.id))


def delete_list(request, list_id):
    tasklist = get_object_or_404(TaskList, pk=list_id)
    tasklist.delete()
    return HttpResponseRedirect('/tasklists/')


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    tasklist = task.task_list
    task.delete()
    return HttpResponseRedirect('/tasklists/{0}/'.format(tasklist.id))