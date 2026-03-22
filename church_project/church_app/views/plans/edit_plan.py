from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from ...models import ReadingPlan
from ...forms import ReadingPlanForm

@permission_required('church_app.can_edit_reading_plan', raise_exception=True)
def edit_plan(request, plan_id):
    plan = ReadingPlan.objects.get(id=plan_id)

    if request.method == 'POST':
        form = ReadingPlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan_detail', plan_id=plan.id)
    else:
        form = ReadingPlanForm(instance=plan)

    return render(request, 'plans/edit_plan.html', {
        'form': form,
        'plan': plan
    })