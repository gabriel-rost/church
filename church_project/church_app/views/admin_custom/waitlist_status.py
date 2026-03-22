from django.shortcuts import render

def waitlist_status(request):
    # Se o usuário for aprovado enquanto está nessa página, 
    # podemos dar um botão de "Ir para a Rede"
    return render(request, 'waitlist/status.html', {
        'user': request.user
    })