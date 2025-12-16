from django.shortcuts import render
from ..models import Channel, FeaturedPost, Post

def home(request):
    channels = Channel.objects.all()
    featured_posts = FeaturedPost.objects.order_by('-id')[:1]
    posts = Post.objects.order_by('-date')[:3]
    return render(request, "home.html", {"channels": channels, "featured_posts": featured_posts, "posts": posts})