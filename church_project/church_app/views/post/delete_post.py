from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from church_app.models import Post

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST' and request.user == post.user:
        channel_pk = post.channel.pk
        post.delete()
        return redirect('post_list', channel_pk=channel_pk)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))