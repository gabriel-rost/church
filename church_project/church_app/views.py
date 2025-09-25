from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Post

from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "church_app/post_list.html", {"posts": posts})

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # comentários principais (parent = None)
    comments = post.comments.filter(parent__isnull=True)
    return render(request, "church_app/post_detail.html", {
        "post": post,
        "comments": comments
    })

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        return HttpResponse("Login successful")
    return render(request, "login.html", {"form": form})