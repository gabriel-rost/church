from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import Post
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