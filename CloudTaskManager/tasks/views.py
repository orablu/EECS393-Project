from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList

def index(request):
    task_list_list = TaskList.objects.order_by('title')
    context = {'task_list_list': task_list_list}
    return render(request, 'tasks/index.html', context)

def details(request, list_id):
    context = {'tasklist': get_object_or_404(TaskList, pk=list_id)}
    return render(request, 'tasks/details.html', context)

def edit(request, list_id):
    context = {'tasklist': get_object_or_404(TaskList, pk=list_id)}
    return render(request, 'tasks/edit.html', context)

def save(request, list_id):
    return HttpResponse("Saved! (not actually though)")
