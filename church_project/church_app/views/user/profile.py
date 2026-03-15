from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()  # Model do User personalizado

@login_required
def get_profile_by_username(request, username):
    user = User.objects.filter(username=username).first()
    return render(request, "profile/user_profile.html", {"user": user})

@login_required
def get_profile_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "profile/user_profile.html", {"user": user})