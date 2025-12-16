from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, max_length=300)
    public = models.BooleanField(default=True)
    roles = models.ManyToManyField('Role', blank=True, related_name="channels")
    members = models.ManyToManyField(User, related_name="channels")

    def __str__(self):
        return self.name