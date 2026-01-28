from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from church_app.models import Post

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # comentários principais (parent = None)
    comments = post.comments.filter(parent__isnull=True)
    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments
    })