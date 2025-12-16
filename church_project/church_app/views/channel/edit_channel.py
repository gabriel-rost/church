from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from church_app.models import Channel

@staff_member_required
def edit_channel(request, channel_pk):
    all_users = User.objects.all()
    channel = get_object_or_404(Channel, pk=channel_pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            channel.name = name
            channel.description = description
            channel.save()
            return redirect('manage_channels')

    context = {
        'all_users': all_users,
        'channel': channel
    }
    return render(request, 'channel/edit_channel.html', context)