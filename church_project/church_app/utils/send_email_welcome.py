import threading
from django.core.mail import send_mail
from django.conf import settings
from decouple import config

site_url = config('SITE_URL', default='http://localhost:8000')

def send_email_welcome(user_username, user_email):
    subject = "Bem-vindo(a) à nossa comunidade"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2c3e50;">Bem-vindo(a), {user_username}</h2>
        <p>Agradecemos por se registrar em nossa comunidade. É uma honra tê-lo(a) conosco.</p>
        <p><a href="{site_url}" style="background-color: #2c3e50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Acessar Aplicativo</a></p>
        <br>
        <p style="font-size: 13px; color: #777;">Atenciosamente,<br><strong>Equipe ChurchApp</strong></p>
    </body>
    </html>
    """
    
    # Função interna para ser executada na Thread
    def send():
        send_mail(
            subject=subject,
            message="", # Texto simples para clientes que não abrem HTML
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_content,
            fail_silently=False,
        )

    # Dispara a Thread
    threading.Thread(target=send).start()