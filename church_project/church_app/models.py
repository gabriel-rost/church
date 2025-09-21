from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ref = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"{self.date} - {self.ref}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_icon = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Content(models.Model):
    title = models.CharField(max_length=256)
    text = models.CharField(max_length=500)
    images = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return self.title

class Channel(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="channels")

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return f"Post de {self.user} em {self.channel} ({self.date})"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500)

    def __str__(self):
        return f"Comentário de {self.user} em {self.post}"

    def is_reply(self):
        return self.parent is not None