from django.db import models
from django.contrib.auth import get_user_model

# Referência ao modelo de usuário ativo no projeto
User = get_user_model()

class ActivityLog(models.Model):
    """
    Modelo de persistência para auditoria de ações no sistema.
    
    Esta classe registra eventos críticos realizados por moderadores ou 
    administradores, permitindo a rastreabilidade de mudanças na plataforma.
    
    Attributes:
        user (ForeignKey): Referência ao :class:`User` que realizou a ação.
        action (CharField): Descrição curta da atividade executada.
        target_id (PositiveIntegerField): ID do objeto afetado (ex: ID de um Post).
        target_type (CharField): Nome da classe do objeto afetado (ex: 'Post').
        timestamp (DateTimeField): Momento exato do registro.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='activities',
        help_text="Usuário responsável pela ação."
    )
    action = models.CharField(
        max_length=255, 
        help_text="Ex: 'Aprovou usuário', 'Ocultou postagem'"
    )
    target_id = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="ID primário do objeto que sofreu a ação."
    )
    target_type = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        help_text="Nome do modelo de destino (ex: 'User', 'Post')."
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Log de Atividade"
        verbose_name_plural = "Logs de Atividades"

    def __str__(self):
        return f"{self.user.username} -> {self.action} ({self.timestamp})"

    
def log_activity(user, action, target=None):
    """
    Função utilitária (Helper) para criação simplificada de registros de log.
    
    Args:
        user (:class:`User`): Instância do usuário que executa a ação.
        action (str): Descrição da tarefa realizada.
        target (models.Model, optional): Instância de qualquer modelo Django que 
            esteja sendo afetado. Extrai automaticamente ID e nome da classe.
            
    Example:
        >>> log_activity(request.user, "Aprovou irmão", target=novo_usuario)
    """
    ActivityLog.objects.create(
        user=user,
        action=action,
        target_id=target.id if target else None,
        target_type=target.__class__.__name__ if target else None
    )