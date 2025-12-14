from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from church_app.forms import ProfileForm, UserForm

@login_required
def edit_user_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('perfil', username=request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form
    }
    return render(request, 'profile/edit_user_profile.html', context)