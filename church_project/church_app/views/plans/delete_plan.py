from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from ...models import ReadingPlan

@staff_member_required
def delete_plan(request, plan_id):
    plan = get_object_or_404(ReadingPlan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list')
    return redirect('plan_list') # Caso tentem acessar via GET