from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from church_app.models import Profile
from django.contrib.auth.models import User

@login_required
def get_profile_by_username(request, username):

    user = User.objects.filter(username=username).first()

    return render(request, "profile/user_profile.html", {"user": user})

@login_required
def get_profile_by_id(request, user_id):

    user = get_object_or_404(User, id=user_id)

    return render(request, "profile/user_profile.html", {"user": user})