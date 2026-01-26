from django.shortcuts import render, get_object_or_404
from ...models import ReadingPlan

def plan_detail(request, plan_id):
    plan = get_object_or_404(ReadingPlan, id=plan_id)
    tasks = plan.tasks.all().prefetch_related('chapters__book')

    # Organizar por semana
    weeks = {}
    for task in tasks:
        weeks.setdefault(task.week_number, []).append(task)

    return render(request, 'plans/plan_detail.html', {
        'plan': plan,
        'weeks': weeks,
    })