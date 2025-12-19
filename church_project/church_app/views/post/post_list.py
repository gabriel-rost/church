from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from church_app.models import Channel

@login_required
def post_list(request, channel_pk):
    channel = get_object_or_404(Channel, pk=channel_pk)
    posts = channel.posts.all().order_by("-date")

    if channel is None:
        return HttpResponse("Canal não encontrado.", status=404)

    if request.user not in channel.members.filter(pk=request.user.pk) and channel.public == False:
        return HttpResponse("Você não tem permissão para ver os posts deste canal.", status=403)

    return render(request, "church_app/post_list.html", {
        "posts": posts,
        "channel": channel
    })