from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.db.models import Exists, OuterRef

from church_app.models import Channel
from church_app.models import Like

@login_required
def post_list(request, channel_pk, page_size=5):
    channel = get_object_or_404(
        Channel.objects.prefetch_related("members"),
        pk=channel_pk
    )

    if page_size > 20:
        page_size = 20  # Limita o tamanho da página para evitar sobrecarga

    # Permissão
    if not channel.public and not channel.members.filter(pk=request.user.pk).exists():
        return HttpResponse("Você não tem permissão para ver este canal.", status=403)

    # Query otimizada
    posts_qs = (
        channel.posts
        .select_related("user",)
        .prefetch_related("attachments",
                          "interactions",
                          "interactions__user")
        .order_by("-date", "-pk")  # Adicione -pk aqui para manter a ordem fixa
    )

    posts_qs = posts_qs.annotate(
    user_has_liked=Exists(
        Like.objects.filter(user=request.user, post=OuterRef('pk'))
        )
    )

    for post in posts_qs:
        post.full_url = request.build_absolute_uri(post.get_absolute_url())

    paginator = Paginator(posts_qs, page_size)  # 5 posts por requisição
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Infinite scroll (AJAX)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "church_app/partials/post_items.html",
            {"posts": page_obj},
            request=request
        )

        return JsonResponse({
            "html": html,
            "has_next": page_obj.has_next()
        })

    # Primeira carga
    return render(request, "church_app/infinite_post_list.html", {
        "posts": page_obj,
        "channel": channel
    })