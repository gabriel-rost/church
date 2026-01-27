from django.db import models
from django.contrib.auth.models import User

class Like(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = 'like', 'Curtir'
        LOVE = 'love', 'Amei'
        HAHA = 'haha', 'Haha'
        WOW = 'wow', 'Uau'
        SAD = 'sad', 'Triste'
        ANGRY = 'angry', 'Grrr'
        PRAY = 'pray', 'Oração'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="interactions")
    type = models.CharField(
        max_length=10, 
        choices=ReactionType.choices, 
        default=ReactionType.LIKE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = "Interação"
        verbose_name_plural = "Interações"

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.post.id}"