from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    """
    Manager customizado para filtrar automaticamente objetos 'excluídos'.
    Referência: :class:`models.Manager`
    """
    def get_queryset(self):
        # Retorna apenas os registros que NÃO possuem data de exclusão
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeleteModel(models.Model):
    """
    Classe abstrata para implementação de Exclusão Lógica.
    
    Attributes:
        deleted_at (DateTimeField): Armazena o momento da exclusão. 
                                   Se null, o objeto está ativo.
    """
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)

    # Manager padrão (mostra apenas os ativos)
    objects = SoftDeleteManager()
    
    # Manager alternativo (para ver TUDO, inclusive os apagados)
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        """
        Sobrescreve o método delete nativo para apenas marcar o campo deleted_at.
        Referência: :meth:`models.Model.delete`
        """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, **kwargs):
        """Apaga o registro permanentemente do banco de dados."""
        super().delete(**kwargs)

    def restore(self):
        """Restaura um item 'excluído'."""
        self.deleted_at = None
        self.save()