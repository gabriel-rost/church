from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from ...models import ReadingPlan
from ...forms import ReadingPlanForm

@staff_member_required
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