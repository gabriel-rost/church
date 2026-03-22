from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ..soft_delete import SoftDeleteModel

class Post(SoftDeleteModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256, blank=True)
    text = models.TextField(blank=True)
    attachments = models.ManyToManyField(
        "church_app.Archive",
        blank=True,
        related_name="posts"
    )

    # RELAÇÃO GENÉRICA (O "Curinga")
    # 1. Aponta para qual TABELA o conteúdo pertence (ReadingPlan, Verse, etc)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    # 2. Armazena o ID do registro naquela tabela
    object_id = models.PositiveIntegerField(null=True, blank=True)
    # 3. O campo que você usará no código para acessar o objeto relacionado
    related_content = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f"Post de {self.user} em {self.channel} ({self.date})"