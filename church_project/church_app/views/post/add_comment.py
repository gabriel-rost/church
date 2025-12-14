from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from church_app.models import Post

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('commentId')

        if not text:
            return redirect('post_detail', post_id=post_id)

        if parent_id:  # é uma resposta
            parent_comment = post.comments.filter(id=parent_id).first()
            if parent_comment:
                post.comments.create(user=request.user, text=text, parent=parent_comment)
        else:  # é um comentário principal
            post.comments.create(user=request.user, text=text)

    return redirect('post_detail', post_id=post_id)