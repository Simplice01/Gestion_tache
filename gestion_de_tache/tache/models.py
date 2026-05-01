from urllib import request

from django.db import models
from django.contrib.auth import get_user_model
from utilisateur.models import Profile
from projet.models import Project
User = get_user_model()



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('in_progress', 'En cours'),
        ('done', 'Terminé'),
        ('valid', 'Validé'),
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
    





        