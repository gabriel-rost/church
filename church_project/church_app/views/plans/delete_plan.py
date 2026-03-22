from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from ...models import ReadingPlan

@permission_required('church_app.can_edit_reading_plan', raise_exception=True)
def delete_plan(request, plan_id):
    plan = get_object_or_404(ReadingPlan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list')
    return redirect('plan_list') # Caso tentem acessar via GET