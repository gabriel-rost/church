from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from church_app.models import Channel, Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def channel_feed(request, channel_pk):
    channel = get_object_or_404(Channel, pk=channel_pk)

    if request.user not in channel.members.all():
        return HttpResponse("Sem permissão", status=403)

    posts_qs = (
        channel.posts
        .select_related("user")
        .prefetch_related("content__attachments")
        .order_by("-date")
    )

    page = int(request.GET.get("page", 1))
    paginator = Paginator(posts_qs, 10)
    posts = paginator.get_page(page)

    # Se for AJAX, retorna JSON
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = {
            "has_next": posts.has_next(),
            "posts": [
                {
                    "id": p.id,
                    "user": p.user.username,
                    "date": p.date.strftime("%d/%m/%Y %H:%M"),
                    "title": p.content.title if p.content and p.content.title else "",
                    "text": p.content.text if p.content else "",
                    "attachments": [
                        {
                            "name": att.file.name,
                            "url": att.file.url
                        } for att in p.content.attachments.all()
                    ] if p.content else [],
                }
                for p in posts
            ]
        }
        return JsonResponse(data)

    # Primeira carga (HTML vazio)
    return render(request, "feed/channel_feed.html", {
        "channel": channel
    })