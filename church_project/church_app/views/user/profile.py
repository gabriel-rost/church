from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def perfil_view(request, username):
    if request.user.username != username:
        return HttpResponse("Você não tem permissão para ver este perfil.", status=403)
    return render(request, "profile/user_profile.html")