from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from ...models import log_activity
from django.contrib.auth import get_user_model
User = get_user_model()

@permission_required('church_app.can_approve_waitlist', raise_exception=True)
def approve_members(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        target_user = get_object_or_404(User, id=user_id)
        
        # Usando o método que você já criou no modelo User
        target_user.approve()
        
        # Registra a ação no nosso sistema de auditoria
        log_activity(request.user, "Aprovou entrada na comunidade", target=target_user)
        
        messages.success(request, f"O irmão {target_user.username} agora faz parte da comunidade!")
        return redirect('approve_members')

    # Busca apenas quem está na lista de espera
    pending_users = User.objects.filter(is_approved=False).order_by('date_joined')
    
    return render(request, 'admin_custom/approve_members.html', {
        'pending_users': pending_users
    })