from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    '''
    Classe User do Django personalizada
    '''
    # O Django já traz username, email, password, first_name, last_name por padrão.
    # Adicionamos apenas o que é específico do seu projeto:
    
    avatar = models.ForeignKey(
        "Archive",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_avatars'
    )
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(
            default=False, 
            verbose_name="Aprovado",
            help_text="Indica se o usuário já saiu da lista de espera."
        )
    accepted_at = models.DateTimeField(
            null=True, 
            blank=True,
            verbose_name="Data de Aceite"
        )
    
    def approve(self):
        """
        Método mestre para aprovação. 
        Garante que ambos os campos sejam atualizados juntos.
        """
        self.is_approved = True
        self.accepted_at = timezone.now()
        self.save()

    class Meta:
        permissions = [
            # Moderação de Comunidade
            ("can_hide_post", "Pode ocultar postagens impróprias"),
            ("can_delete_comment", "Pode excluir comentários ofensivos"),
            ("can_approve_waitlist", "Pode aprovar novos irmãos na lista de espera"),
            
            # Gestão de Conteúdo
            ("can_create_reading_plan", "Pode criar e publicar planos de leitura oficiais"),
            ("can_edit_reading_plan", "Pode editar planos de leitura existentes"),
            
            # Gestão de Usuários (Nível Moderador)
            ("can_mute_user", "Pode silenciar usuários por tempo determinado"),
            ("can_report_review", "Pode analisar denúncias de usuários"),
        ]

    def __str__(self):
        return self.get_full_name() or self.username