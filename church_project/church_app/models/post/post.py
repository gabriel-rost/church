from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey("Content", on_delete=models.CASCADE)

    class Meta:
        ordering = ["user"]

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f"Post de {self.user} em {self.channel} ({self.date})"