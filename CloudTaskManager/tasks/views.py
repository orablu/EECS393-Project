from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task
from tasks.forms import TaskForm


def index(request):
    context = {'task_list_list': TaskList.objects.order_by('title')}
    return render(request, 'tasks/index.html', context)


def details(request, list_id):
	try:
		tasklist = TaskList.objects.get(pk=list_id)
		tasks_list = tasklist.task_set.all()
		context = {'tasklist': tasklist,
			'tasks_list': tasks_list,
			'list_id': list_id}
	except:
		raise Http404
	return render(request, 'tasks/details.html', context)


def edit(request, list_id):
	if request.method == 'POST':
		tasklist, created = TaskList.objects.get_or_create(pk=list_id)
		task = Task(task_list=tasklist)
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/tasklists/' + list_id + '/')
	else:
		form = TaskForm()
	return render(request, 'tasks/edit.html', {'form': form,})


def save(request, list_id):
    return HttpResponse("Saved! (not actually though)")
