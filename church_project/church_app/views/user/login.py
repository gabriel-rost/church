from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        return HttpResponse("Login successful")
    return render(request, "login.html", {"form": form})