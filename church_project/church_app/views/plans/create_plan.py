from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from ...models import ReadingPlan
from ...forms import ReadingPlanForm
from django.contrib.auth import get_user_model
User = get_user_model()
from ...models import ReadingPlan, Post, log_activity, Channel
from django.contrib import messages

@permission_required('church_app.can_create_reading_plan', raise_exception=True)
def create_plan(request):
    if request.method == 'POST':
        form = ReadingPlanForm(request.POST, request.FILES)
        if form.is_valid():
            new_plan = form.save(commit=False)
            
            new_plan.author = request.user
            
            new_plan.save()

            if new_plan.is_published:
                from ...services.notifications import trigger_notifications # Import local para evitar circularidade
                users = User.objects.filter(is_active=True)
                trigger_notifications(users, new_plan)

                # Criar Post no feed

                channel = get_object_or_404(Channel, pk=1)

                Post.objects.create(
                    user=request.user,
                    title=f"📖 Novo Plano: {new_plan.title}",
                    text="Confira nossa nova jornada de leitura!",
                    channel=channel,
                    related_content=new_plan
                )

                log_activity(request.user, f"Publicou o plano: {new_plan.title}", target=new_plan)
                messages.success(request, f"O plano '{new_plan.title}' foi publicado com sucesso!")

            return redirect('plan_detail', plan_id=new_plan.id)
    else:
        form = ReadingPlanForm()
    return render(request, 'plans/create_plan.html', {'form': form})