from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TodoItem
import json

def todo_list(request):
    todos = TodoItem.objects.all()
    return render(request, 'todos/todo_list.html', {'todos': todos})

def add_todo(request):
    if request.method == 'POST':
        title = request.POST['title']
        TodoItem.objects.create(title=title)
        return redirect('todo_list')
    return render(request, 'todos/add_todo.html')

@csrf_exempt  # Note: Remove this in production and use proper CSRF protection
def toggle_todo(request, todo_id):
    if request.method == 'POST':
        try:
            todo = TodoItem.objects.get(id=todo_id)
            data = request.body.decode('utf-8')
            completed = json.loads(data).get('completed', False)
            todo.completed = completed
            todo.save()
            return JsonResponse({'status': 'success'})
        except TodoItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Todo not found'}, status=404)
    return redirect('todo_list')

def delete_todo(request, todo_id):
    TodoItem.objects.get(id=todo_id).delete()
    return redirect('todo_list')
