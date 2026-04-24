from django import forms
from .models import Profile, Task,Project
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm




class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la tâche', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description de la tâche'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'project': forms.Select(attrs={'class': 'form-select', 'required': True})
        }

