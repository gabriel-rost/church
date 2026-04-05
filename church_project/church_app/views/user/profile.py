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



from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from ...models import Post

def user_posts_ajax(request, username):
    target_user = get_object_or_404(User, username=username)
    # Buscamos apenas posts públicos do usuário
    posts = Post.objects.filter(user=target_user, public=True).order_by('-date')[:10]
    
    # Renderizamos um template parcial apenas com os cards
    html = render_to_string('post/includes/post_cards_partial.html', {
        'posts': posts,
        'request': request
    })
    
    return JsonResponse({'html': html})