from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from ..models import Post
from django.contrib.auth import get_user_model
User = get_user_model()

def send_new_plan_notification(plan):
    print("Iniciando envio de e-mail estilizado...")

    post = Post.objects.filter(content_type__model='readingplan', object_id=plan.id).first()
    
    # Se o post existir, usamos a URL dele, caso contrário a do plano
    target_url = f"{settings.SITE_URL}{post.get_absolute_url()}" if post else f"{settings.SITE_URL}{plan.get_absolute_url()}"

    members = User.objects.filter(is_active=True, is_approved=True)
    recipient_list = list(members.values_list('email', flat=True))

    if not recipient_list:
        print("Nenhum destinatário encontrado.")
        return

    subject = f"📖 Novo Plano: {plan.title}"
    from_email = settings.DEFAULT_FROM_EMAIL

    context = {
        'plan': plan,
        'url': target_url,
        'church_name': "Nossa Igreja"
    }

    html_content = render_to_string('emails/new_plan_notification.html', context)
    text_content = strip_tags(html_content)

    for email in recipient_list:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
    
    print(f"Emails enviados para {len(recipient_list)} membros.")