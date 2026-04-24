
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Group, Permission, User
from .models import Profile
from tache.models import Task, Project  


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
    # PROJECT
    'add_project': 'Créer un projet',
    'change_project': 'Modifier un projet',
    'delete_project': 'Supprimer un projet',
    'view_project': 'Voir un projet',
    'change_project_status': 'Changer le statut du projet',
    'finalize_project': 'Finaliser un projet',

    # TASK
    'add_task': 'Créer une tâche',
    'change_task': 'Modifier une tâche',
    'delete_task': 'Supprimer une tâche',
    'view_task': 'Voir une tâche',
    'assign_task': 'Assigner une tâche',
    'change_task_status': 'Changer le statut d’une tâche',

    # COMMENT
    'add_comment': 'Créer un commentaire',
    'change_comment': 'Modifier un commentaire',
    'delete_comment': 'Supprimer un commentaire',
    'view_comment': 'Voir un commentaire',

    # USER (auth)
    'add_user': 'Créer un utilisateur',
    'change_user': 'Modifier un utilisateur',
    'delete_user': 'Supprimer un utilisateur',
    'view_user': 'Voir un utilisateur',

    # GROUP (roles)
    'add_group': 'Créer un rôle',
    'change_group': 'Modifier un rôle',
    'delete_group': 'Supprimer un rôle',
    'view_group': 'Voir un rôle',

    # PERMISSION
    'add_permission': 'Créer une permission',
    'change_permission': 'Modifier une permission',
    'delete_permission': 'Supprimer une permission',
    'view_permission': 'Voir une permission',

    # PROFILE
    'add_profile': 'Créer un profil',
    'change_profile': 'Modifier un profil',
    'delete_profile': 'Supprimer un profil',
    'view_profile': 'Voir un profil',

    # LOG ENTRY (admin)
    'add_logentry': 'Ajouter une entrée de journal',
    'change_logentry': 'Modifier une entrée de journal',
    'delete_logentry': 'Supprimer une entrée de journal',
    'view_logentry': 'Voir une entrée de journal',

    # CONTENT TYPE
    'add_contenttype': 'Créer un type de contenu',
    'change_contenttype': 'Modifier un type de contenu',
    'delete_contenttype': 'Supprimer un type de contenu',
    'view_contenttype': 'Voir un type de contenu',

    # SESSION
    'add_session': 'Créer une session',
    'change_session': 'Modifier une session',
    'delete_session': 'Supprimer une session',
    'view_session': 'Voir une session',
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



class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Adresse e-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre adresse e-mail'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        })
    )
    new_password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez le mot de passe'
        })
    )       
 