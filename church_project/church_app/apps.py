from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ChurchAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'church_app'

    def ready(self):
        import church_app.signals
        # Conecta a criação do canal
        post_migrate.connect(create_default_channel, sender=self)
        post_migrate.connect(create_church_roles, sender=self)

def create_default_channel(sender, **kwargs):
    from .models import Channel
    Channel.objects.get_or_create(
        name="geral",
        defaults={
            "description": "Canal geral da comunidade",
            "public": True,
        },
    )

def create_church_roles(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    
    roles = {
        'Moderador': [
            'can_hide_post', 'can_delete_comment', 
            'can_approve_waitlist', 'can_mute_user', 'can_report_review',
            'can_create_reading_plan', 'can_edit_reading_plan'
        ],
        'Curador de Conteúdo': [
            'can_create_reading_plan', 'can_edit_reading_plan'
        ]
    }

    for role_name, permissions in roles.items():
        group, created = Group.objects.get_or_create(name=role_name)
        perms = Permission.objects.filter(codename__in=permissions)
        group.permissions.set(perms)