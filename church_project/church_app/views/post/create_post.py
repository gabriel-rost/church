from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from church_app.models import Channel, Post, Archive
from church_app.forms import PostForm
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError

@login_required
@transaction.atomic
def create_post(request, channel_pk):
    channel = get_object_or_404(Channel, pk=channel_pk)

    if not channel.members.filter(pk=request.user.pk).exists() and not channel.public:
        return HttpResponseForbidden("Você não tem permissão para postar neste canal.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)

            new_post.user = request.user
            new_post.channel = channel
            new_post.save()

            for uploaded_file in request.FILES.getlist('attachments'):
                archive = Archive.objects.create(file=uploaded_file)
                new_post.attachments.add(archive)

            return redirect('infinite_post_list', channel_pk=channel.pk)

    else:
        initial = {}
        if "text" in request.GET:
            initial["text"] = request.GET.get("text")

        form = PostForm(initial=initial)

    return render(request, 'create_post.html', {
        'form': form,
        'channel': channel,
    })