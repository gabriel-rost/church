import threading
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from webpush import send_user_notification
from decouple import config

URL = config('SITE_URL', default='http://localhost:8000')

# Função auxiliar para rodar o loop pesado em background
def broadcast_notification(users, payload):
    for user in users:
        try:
            # Sua função original de envio (WebPush / Firebase / etc)
            send_user_notification(user=user, payload=payload, ttl=1000)
        except Exception as e:
            print(f"Erro ao enviar para {user.username}: {e}")

@user_passes_test(lambda u: u.is_superuser)
def send_notification_view(request):
    if request.method == "POST":
        head = request.POST.get("head", "⛪ Novo Aviso")
        body = request.POST.get("body", "")

        if not body:
            return HttpResponse("Erro: A mensagem não pode estar vazia.", status=400)

        payload = {
            "head": head,
            "body": body,
            "icon": "https://api.iconify.design/token-branded:blue.svg",
            "url": "/"
        }

        # Pegamos todos os usuários ativos
        users = User.objects.filter(is_active=True)

        # Disparamos o processo em uma Thread para não travar a tela do admin
        threading.Thread(target=broadcast_notification, args=(users, payload)).start()

        return HttpResponse(f"Sucesso! A notificação está sendo enviada para {users.count()} usuários.<br> Você pode fechar esta janela. <a href='{URL}'>Clique aqui para voltar ao site</a>")

    return render(request, "send_notification.html")