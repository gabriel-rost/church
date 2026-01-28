from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from church_app.models import Post, Like

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        is_liked = False
    else:
        is_liked = True

    return JsonResponse({
        'liked': is_liked,
        'like_count': post.interactions.count()
    })