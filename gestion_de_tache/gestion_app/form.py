from django import forms
from .models import Profile, Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission, User
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


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        strip=False, 
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')        

PERMISSION_TRANSLATIONS = {
    'add_task': 'Créer une tâche',
    'change_task': 'Modifier une tâche',
    'delete_task': 'Supprimer une tâche',
    'view_task': 'Voir une tâche',
    'assign_task': 'Assigner une tâche',
    'change_task_status': 'Changer le statut d’une tâche',
    'add_comment': 'Créer un commentaire',
    'change_comment': 'Modifier un commentaire',
    'delete_comment': 'Supprimer un commentaire',
    'view_comment': 'Voir un commentaire',
}


class RoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        translated_choices = []
        for permission in self.fields['permissions'].queryset:
            label = PERMISSION_TRANSLATIONS.get(permission.codename, permission.name)
            translated_choices.append((permission.id, label))

        self.fields['permissions'].choices = translated_choices


class ProfileRoleForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']        