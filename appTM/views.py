from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .tasks import send_task_reminder
from django.core.cache import cache
import hashlib

def signup_view(request): # View to create user account
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required(login_url='login')
def home(request): # view to take user to my main page
    return render(request, 'appTM/base.html')

@login_required
def task_list(request): # view to take user to uncomplete tasks list
    category = request.GET.get('category', '').strip().lower()
    user = request.user
    cache_key = f"user_{user.id}_tasks_active_{category or 'all'}"

    tasks = cache.get(cache_key)

    if tasks is None:
        base_queryset = Task.objects.filter(user=user, completed=False)
        tasks = base_queryset.filter(category=category).order_by('due_date') if category else base_queryset.order_by('due_date')
        cache.set(cache_key, tasks, timeout=60 * 5)  # Cache for 5 minutes

    categories = Task.objects.filter(user=user, completed=False).exclude(category__isnull=True).exclude(category__exact='') \
        .values_list('category', flat=True).distinct()

    return render(request, 'appTM/tasks_list.html', {
        'tasks': tasks,
        'categories': categories,
        'selected_category': category
    })

@login_required
def tasks_complete(request): # view to take user to completed tasks list
    category = request.GET.get('category', '').strip().lower()
    user = request.user
    cache_key = f"user_{user.id}_tasks_complete_{category or 'all'}"

    tasks = cache.get(cache_key)

    if tasks is None: # if cache is empty tasks are pulled from db and cache is created
        base_queryset = Task.objects.filter(user=user, completed=True)
        tasks = base_queryset.filter(category=category).order_by('due_date') if category else base_queryset.order_by('due_date')
        cache.set(cache_key, tasks, timeout=60 * 5)

    categories = Task.objects.filter(user=user, completed=True).exclude(category__isnull=True).exclude(category__exact='') \
        .values_list('category', flat=True).distinct()

    return render(request, 'appTM/tasks_complete.html', {
        'tasks': tasks,
        'categories': categories,
        'selected_category': category
    })


@login_required(login_url='login')
def task_create(request): # view to create a task and populate the list with it
    form = TaskForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            send_task_reminder.delay(task.id, 'created')
            cache.delete(f"user_{request.user.id}_tasks_active_all")
            return redirect('task_list')  # Only redirects the user if it's a valid model entry
        else:
            #  Does not redirect user and re-renders the form with error
            pass
    return render(request, 'appTM/tasks_form.html', {'form': form})

def task_delete(request, pk): # view to delete a task without saving or moving to complete_list
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    cache.delete(f"user_{request.user.id}_tasks_active_all")
    return redirect('task_list')

def complete_task(request, pk): # view to complete a task and move it to the completed list
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save()
    send_task_reminder.delay(task.id, 'completed')
    cache.delete(f"user_{request.user.id}_tasks_active_all")
    return redirect('task_list')

def uncomplete_task(request, pk): # view to reopen a task and move it to the task list
    task = get_object_or_404(Task, pk=pk)
    task.completed = False
    task.save()
    send_task_reminder.delay(task.id, 'uncompleted')
    cache.delete(f"user_{request.user.id}_tasks_active_all")
    return redirect('tasks_complete')

def task_flag(request, pk): # view to flag important tasks so that they are more visible in task_list
    task = get_object_or_404(Task, pk=pk)
    task.flagged = not task.flagged
    task.save()
    send_task_reminder.delay(task.id, 'flagged')
    cache.delete(f"user_{request.user.id}_tasks_active_all")
    return redirect('task_list')
