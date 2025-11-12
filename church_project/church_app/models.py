from datetime import datetime
import os
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import FileExtensionValidator, RegexValidator, MaxLengthValidator

# Create your models here.

# Metodos auxiliares para upload de arquivos podem ser adicionados aqui se necessário. Refatorar depois..

# Validador para nomes de arquivos: apenas letras, números, "_" e "-"
filename_validator = RegexValidator(
    regex=r'^[\w-]+$',
    message='O nome do arquivo só pode conter letras, números, "_" e "-"'
)

# Função para upload com timestamp e substituição de espaços por "_"
def upload_to_with_timestamp(instance, filename):
    base, ext = os.path.splitext(filename)
    # Substitui espaços por underline
    base = base.replace(" ", "_")
    # Remove caracteres inválidos (apenas alfanumérico, "_" e "-")
    safe_base = "".join(c for c in base if c.isalnum() or c in ("_", "-"))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"archives/{safe_base}_{timestamp}{ext}"

class Archive(models.Model):
    file = models.FileField(
        upload_to=upload_to_with_timestamp,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf']),
            MaxLengthValidator(100),
            filename_validator
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def size(self):
        return self.file.size

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ForeignKey(
        Archive,
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


class Content(models.Model):
    title = models.CharField(max_length=256, blank=True)
    text = models.TextField(blank=False)
    attachments = models.ManyToManyField(Archive, blank=True, related_name='contents')

    def __str__(self):
        return self.text[:50]  # Retorna os primeiros 50 caracteres do texto como representação

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