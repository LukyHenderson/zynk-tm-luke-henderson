from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm): # Task creation form
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category']


class CustomUserCreationForm(UserCreationForm): # User creation form
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
