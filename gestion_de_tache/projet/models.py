from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
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
