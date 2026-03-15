from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    # O Django já traz username, email, password, first_name, last_name por padrão.
    # Adicionamos apenas o que é específico do seu projeto:
    
    avatar = models.ForeignKey(
        "Archive",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_avatars'
    )
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username