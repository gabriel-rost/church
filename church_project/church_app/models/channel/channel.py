from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.TextField(blank=True, max_length=300)
    public = models.BooleanField(default=True, db_index=True)
    members = models.ManyToManyField(
    User,
    through="ChannelMember",
    related_name="channels"
    )

    def __str__(self):
        return self.name