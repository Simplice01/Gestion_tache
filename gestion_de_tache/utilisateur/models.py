from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
# Create your models here.
User = get_user_model()

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

    def has_permission(self, permission_codename, app_label='tache'):
        if self.role is None:
            return False
        return self.role.permissions.filter(
            codename=permission_codename,
            content_type__app_label=app_label
        ).exists()
    


