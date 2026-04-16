from urllib import request

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

User = get_user_model()


class Project(models.Model):
    STATUS_CHOICES = [
        ('debut', 'Début'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('finalise', 'Finalisé'),
    ]

    name_project = models.CharField(max_length=255)
    deadline = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='debut')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )

    def __str__(self):
        return self.name_project

    def all_tasks_completed(self):
        tasks = self.tasks.all()
        if not tasks.exists():
            return False
        return not tasks.exclude(status='done').exists()

    def clean(self):
        if self.statut == 'termine' and not self.all_tasks_completed():
            raise ValidationError(
                "Impossible de mettre ce projet à 'Terminé' tant que toutes les tâches ne sont pas terminées."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
    ]
    project = models.ForeignKey(
    Project,
    on_delete=models.CASCADE,
    related_name='tasks'
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.task.title}'
    

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profiles'
    )

    def __str__(self):
        return f"Profil de {self.user.username}"

    def has_permission(self, permission_codename, app_label='gestion_app'):
        if self.role is None:
            return False
        return self.role.permissions.filter(
            codename=permission_codename,
            content_type__app_label=app_label
        ).exists()
    







        