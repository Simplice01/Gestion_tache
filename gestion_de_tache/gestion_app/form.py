from django import forms
from .models import Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la tâche', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description de la tâche'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }