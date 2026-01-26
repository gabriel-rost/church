from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Adicionamos uma mensagem de sucesso que o Django guarda para a próxima página
    messages.success(request, "Até logo! Você saiu com segurança.")
    return redirect('login')