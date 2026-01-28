from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from church_app.models import Post

@login_required
def post_likers(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Buscamos as interações trazendo os dados do usuário para ser rápido
    likes = post.interactions.select_related('user').all().order_by('-created_at')
    
    return render(request, 'church_app/partials/likers_modal_content.html', {
        'likes': likes,
        'post': post
    })