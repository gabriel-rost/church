from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction
from church_app.forms import SignUpForm

@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Perfil é criado automaticamente via signals
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})