
from gestion_de_tache.utilisateur import forms
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name_project', 'deadline']
        widgets = {
            'name_project': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du projet'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class UpdateStatusProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['statut']
        widgets = {
            'statut': forms.Select(attrs={
                'class': 'form-select'
            }),
        }