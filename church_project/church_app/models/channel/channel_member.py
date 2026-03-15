from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group

class ChannelMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    channel = models.ForeignKey(
        "church_app.Channel",
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "channel")

    def __str__(self):
        return f"{self.user} em {self.channel} ({self.role})"