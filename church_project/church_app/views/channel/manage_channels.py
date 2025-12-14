from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from church_app.models import Channel

@staff_member_required
def manage_channels(request):
    channels = Channel.objects.all()
    return render(request, 'manage_channels.html', {'channels': channels})