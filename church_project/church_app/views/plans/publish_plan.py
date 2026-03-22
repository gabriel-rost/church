from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from ...models import ReadingPlan, Post, log_activity, Channel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import get_user_model
User = get_user_model()

from ...signals import handle_plan_publication

@login_required
@permission_required('church_app.can_edit_reading_plan', raise_exception=True)
def publish_plan(request, plan_id):
    if request.method == "POST":
        plan = get_object_or_404(ReadingPlan, id=plan_id)
        channel = get_object_or_404(Channel, pk=1)

        if plan.is_published:
            messages.info(request, "Este plano já está publicado.")
            return redirect('plan_list')

        # 1. Salva o status primeiro
        plan.is_published = True
        plan.published_at = timezone.now()
        
        # 2. Só dispara se ainda não foi enviado
        if not plan.notification_sent:
            from ...services.notifications import trigger_notifications # Import local para evitar circularidade
            
            users = User.objects.filter(is_active=True)
            trigger_notifications(users, plan)
            
            #plan.notification_sent = True
        
        plan.save()

        # 3. Cria o Post no Feed
        Post.objects.create(
            user=request.user,
            title=f"📖 Novo Plano: {plan.title}",
            text="Confira nossa nova jornada de leitura!",
            channel=channel,
            related_content=plan
        )

        log_activity(request.user, f"Publicou o plano: {plan.title}", target=plan)
        messages.success(request, f"O plano '{plan.title}' foi publicado com sucesso!")
    
    return redirect('plan_list')