from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from church_app.models import Post, FeaturedPost

@staff_member_required
def add_featured_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    FeaturedPost.objects.get_or_create(post=post)
    return redirect('post_detail', post_id=post_id)