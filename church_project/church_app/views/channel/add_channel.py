from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from church_app.models import Channel

@staff_member_required
def add_channel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            Channel.objects.create(name=name, description=description)
            return redirect('manage_channels')

    return render(request, 'channel/add_channel.html')