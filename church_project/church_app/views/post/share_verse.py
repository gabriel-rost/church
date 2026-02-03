from django.shortcuts import get_object_or_404, redirect, render
from church_app.models import Channel
from church_app.forms import ContentForm
from church_app.models.post.post import Post

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

def share_verse(request):
    text = request.GET.get("text", "")

    url = reverse("create_post", args=[1])  # channel_id
    query = urlencode({"text": text})

    return redirect(f"{url}?{query}")
