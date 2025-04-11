from django.db import models
from django.contrib.auth.models import User

class Task(models.Model): # task model for generating tasks with task_form
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Links model to specific users for security/privacy
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True) # used to order tasks chronologically by due_date on task_list
    completed = models.BooleanField(default=False) # used to move task between task_list and completed_task_list
    category = models.CharField(max_length=20) # category argument useful for category sorting in task_list
    flagged = models.BooleanField(default=False) # used to flag tasks in task_list

    def __str__(self): # Prints task as task.title instead of as a python object.
        return self.title