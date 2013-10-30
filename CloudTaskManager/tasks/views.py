from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from tasks.models import TaskList, Task


def index(request):
    context = {'task_list_list': TaskList.objects.order_by('title')}
    return render(request, 'tasks/index.html', context)


def details(request, list_id):
    context = {'tasklist': get_object_or_404(TaskList, pk=list_id)}
    return render(request, 'tasks/details.html', context)


def edit_list(request, list_id):
    context = {'tasklist': get_object_or_404(TaskList, pk=list_id)}
    return render(request, 'tasks/edit_list.html', context)


def edit_task(request, task_id):
    context = {'task': get_object_or_404(Task, pk=task_id)}
    return render(request, 'tasks/edit_task.html', context)


def new_task(request, list_id):
    context = {'list_id': list_id}
    return render(request, 'tasks/new_task.html', context)


def save_list(request):
    return HttpResponse("Saved! (not actually though)")


def save_task(request):
    return HttpResponse("Saved! (not actually though)")


def save_new_task(request):
    return HttpResponse("Saved! (not actually though)")
