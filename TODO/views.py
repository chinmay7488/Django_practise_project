from django.shortcuts import render, redirect
from .models import TaskDetails
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def Home(request):
    task = TaskDetails.objects.all()
    data ={
        'tasks' : task,
        'pending_count' : task.filter(Is_Completed=False).count(),
        'completed_count' : task.filter(Is_Completed=True).count(),
    }

    return render(request, 'TODO/task_list.html', data)

def Create_EditTask(request, task_id=0):
    context={}
    if task_id != 0 :
        task = TaskDetails.objects.get(id=task_id)
        context = {
            'task' : task,
            }

    if request.method == "POST":
        print(request.POST)
        Title = request.POST.get('task_text')
        Priority = request.POST.get('priority')
        Due_date = request.POST.get('due_date')
        Is_completed = request.POST.get('is_complete') == 'on'

        if task_id  != 0 :
            task = TaskDetails.objects.get(id=task_id)
            task.Title = request.POST.get('task_text')
            task.Priority = request.POST.get('priority')
            task.Due_Date = request.POST.get('due_date')
            task.Is_Completed = request.POST.get('is_complete') == 'on'
            task.save()
        else:
            TaskDetails.objects.create(
                Title = Title,
                Due_Date = Due_date,
                Is_Completed = Is_completed,
                Priority = Priority
            )

        return redirect('TODO:home')

    return render(request, 'TODO/task_form.html', context)

def DeleteTask(request, task_id):
    if request.method == "POST":
        task = TaskDetails.objects.get(id = task_id)
        task.delete() 
        return redirect('TODO:home')

    return render(request, 'TODO/task_confirm_delete.html')

def toggle_task_status(request, task_id):
    if request.method == "POST":
        task = TaskDetails.objects.get(id = task_id)
        
        # Get data from the JSON body
        data = json.loads(request.body)
        task.Is_Completed = data.get('is_completed')
        task.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
