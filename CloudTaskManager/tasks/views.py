from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task
from tasks.forms import TaskForm

def index(request):
    task_list_list = TaskList.objects.order_by('title')
    context = {'task_list_list': task_list_list}
    return render(request, 'tasks/index.html', context)

def details(request, list_id):
	try:
		tasklist = TaskList.objects.get(pk=list_id)
		tasks_list = tasklist.task_set.all()
		context = {'tasklist': tasklist, 'tasks_list': tasks_list}
	except:
		raise Http404
	return render(request, 'tasks/details.html', context)

def edit(request, list_id):
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			form.save(title, description)

def save(request, list_id):
    return HttpResponse("Saved! (not actually though)")
