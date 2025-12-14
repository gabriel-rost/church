from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from church_app.models import Channel
from django.contrib.auth.models import User

@staff_member_required
def manage_channel_members(request, channel_pk):
    channel = get_object_or_404(Channel, pk=channel_pk)
    
    # Busca todos os usuários, exceto os que JÁ ESTÃO no canal
    # (Otimização: use o ORM para filtrar)
    channel_members_pks = channel.members.values_list('pk', flat=True)
    non_members = User.objects.exclude(pk__in=channel_members_pks).all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user_to_manage = get_object_or_404(User, pk=user_id)
        
        if action == 'add':
            channel.members.add(user_to_manage)
        elif action == 'remove':
            channel.members.remove(user_to_manage)
        
        # Redireciona para evitar re-submissão do formulário
        return redirect('manage_channel_members', channel_pk=channel_pk)

    context = {
        'channel': channel,
        # O Django fornece channel.members.all automaticamente
        'non_members': non_members,
    }
    return render(request, 'channel/manage_channel_members.html', context)