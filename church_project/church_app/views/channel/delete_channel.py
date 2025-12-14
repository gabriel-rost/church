from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from church_app.models import Channel

@staff_member_required
def delete_channel(request, channel_pk):
    if request.method == 'POST':
        channel = get_object_or_404(Channel, pk=channel_pk)
        channel.posts.all().delete()  # Deleta todos os posts associados ao canal
        channel.delete()
        return redirect('manage_channels')
    return HttpResponse("Método não permitido", status=405)