from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import get_user_model
from ...models import log_activity

User = get_user_model()

@permission_required('church_app.can_approve_waitlist', raise_exception=True)
def manage_permissions(request):
    available_groups = Group.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        target_user = get_object_or_404(User, id=user_id)

        # Proteção contra alteração de Superuser ou de si mesmo
        if target_user.is_superuser or target_user.id == request.user.id:
            messages.error(request, "Ação não permitida para este usuário.")
            return redirect('manage_permissions')
        
        # 1. Atualização das permissões no Banco de Dados
        target_user.groups.clear()
        
        if group_id:
            new_group = get_object_or_404(Group, id=group_id)
            target_user.groups.add(new_group)
            msg = f"Cargo de {target_user.username} alterado para {new_group.name}."
        else:
            msg = f"{target_user.username} agora é um Membro Comum."

        # 2. Invalidação de Sessão
        # Buscamos todas as sessões ativas e deletamos as que pertencem ao target_user
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            data = session.get_decoded()
            if str(target_user.pk) == data.get('_auth_user_id'):
                session.delete()
            
        # 3. Auditoria e Feedback
        log_activity(request.user, msg, target=target_user)
        messages.success(request, msg)
        return redirect('manage_permissions')

    # GET: Listagem de membros
    active_members = User.objects.filter(
        is_approved=True
    ).exclude(
        is_superuser=True
    ).exclude(
        id=request.user.id
    ).prefetch_related('groups').order_by('username')
    
    return render(request, 'admin_custom/manage_permissions.html', {
        'members': active_members,
        'groups': available_groups
    })