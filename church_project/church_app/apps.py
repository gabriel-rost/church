from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ChurchAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'church_app'

    def ready(self):
        import church_app.signals
        post_migrate.connect(create_default_channel, sender=self)

def create_default_channel(sender, **kwargs):
    from .models import Channel

    Channel.objects.get_or_create(
        name="geral",
        defaults={
            "description": "Canal geral da comunidade",
            "public": True,
        },
    )