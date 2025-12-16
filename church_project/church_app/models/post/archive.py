from datetime import datetime
from django.db import models
import os
from django.core.validators import FileExtensionValidator, RegexValidator, MaxLengthValidator
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