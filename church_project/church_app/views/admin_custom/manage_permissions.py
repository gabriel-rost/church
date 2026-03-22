from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib import messages
from ...models import log_activity
from django.contrib.auth import get_user_model
User = get_user_model()

@permission_required('church_app.can_approve_waitlist', raise_exception=True)
def manage_permissions(request):
    # Buscamos os cargos disponíveis (Moderador, Curador, etc)
    available_groups = Group.objects.all()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        target_user = get_object_or_404(User, id=user_id)

        if target_user.is_superuser:
            messages.error(request, "Não é permitido alterar as permissões de um Administrador Geral.")
            return redirect('manage_permissions')
        
        # 1. Limpa cargos anteriores para evitar conflito de permissões
        target_user.groups.clear()
        
        # 2. Atribui o novo cargo se houver um selecionado
        if group_id:
            new_group = get_object_or_404(Group, id=group_id)
            target_user.groups.add(new_group)
            msg = f"Cargo de {target_user.username} alterado para {new_group.name}."
        else:
            msg = f"{target_user.username} agora é um Membro Comum."
            
        # 3. Registrar a alteração no Log de Auditoria
        log_activity(request.user, msg, target=target_user)
        
        messages.success(request, msg)
        return redirect('manage_permissions')

    # Listamos apenas usuários aprovados para focar na gestão de quem já é da casa
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