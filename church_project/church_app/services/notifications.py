import threading
from django.db import connection
from webpush import send_user_notification

def send_plan_notifications_task(users_list, plan_title, plan_url):
    """Lógica que roda em background"""
    print("notifications.py --- Executando: send_plan_notifications_task")
    try:
        payload = {
            "icon": "https://api.iconify.design/token-branded:blue.svg",
            "head": f"📖 Novo Plano: {plan_title}",
            "body": "Uma nova jornada de leitura começou. Confira!",
            "url": plan_url
        }
        for user in users_list:
            try:
                send_user_notification(user=user, payload=payload)
                pass 
            except Exception as e:
                print(f"Erro ao notificar {user}: {e}")
    finally:
        connection.close()

def trigger_notifications(users, plan):
    """Função chamada pela View"""
    users_list = list(users)

    plan_url = plan.get_absolute_url()
    plan_title = plan.title

    thread = threading.Thread(
        target=send_plan_notifications_task, 
        args=(users_list, plan_title, plan_url)
    )
    thread.setDaemon(True)
    thread.start()