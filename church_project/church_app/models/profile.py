from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(
        "Archive",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profile_avatars'
    )
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)        # descrição opcional
    phone = models.CharField(max_length=20, blank=True)  # telefone opcional
    location = models.CharField(max_length=100, blank=True)  # cidade/estado opcional

    def __str__(self):
        return f"Perfil de {self.user.username}"