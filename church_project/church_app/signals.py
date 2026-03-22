from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReadingPlan
from .services import send_new_plan_notification
import threading
from django.db import connection

@receiver(post_save, sender=ReadingPlan)
def handle_plan_publication(sender, instance, created, **kwargs):
    if instance.is_published and not instance.notification_sent:
        # Criamos a thread aqui dentro
        def run_in_background():
            try:
                send_new_plan_notification(instance)
                # Marcar como enviado usando .update para evitar novo signal
                ReadingPlan.objects.filter(pk=instance.pk).update(notification_sent=True)
            finally:
                connection.close()

        thread = threading.Thread(target=run_in_background)
        thread.start()