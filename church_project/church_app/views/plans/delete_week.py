from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from ...models import ReadingPlan, PlanTask

@staff_member_required
def delete_week(request, plan_id, week_number):
    plan = get_object_or_404(ReadingPlan, id=plan_id)
    if request.method == 'POST':
        # Apaga todas as tarefas desse plano que pertencem à semana selecionada
        PlanTask.objects.filter(plan=plan, week_number=week_number).delete()
    return redirect('plan_detail', plan_id=plan.id)