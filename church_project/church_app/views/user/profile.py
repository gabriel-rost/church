from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def perfil_view(request, username):
    return render(request, "profile/user_profile.html")