from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Archive(models.Model):
    # O FileField gerencia o upload e o caminho do arquivo.
    # O nome original, tamanho e tipo podem ser acessados a partir deste campo.
    file = models.FileField(upload_to="archives/")
    
    # Campo para registrar quando o upload foi feito.
    # auto_now_add=True garante que a data seja salva na criação.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Retorna o caminho base do arquivo, que é mais útil.
        # ex: "archives/meu_documento.pdf"
        return self.file.name

    @property
    def filename(self):
        # Propriedade para obter apenas o nome do arquivo, sem o caminho.
        import os
        return os.path.basename(self.file.name)

    @property
    def size(self):
        # Propriedade para acessar o tamanho do arquivo diretamente.
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
    title = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    attachments = models.ManyToManyField(Archive, blank=True, related_name='contents')

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