from django.shortcuts import render, get_object_or_404
from ...models import ReadingPlan, UserTaskProgress

from django.contrib.auth.decorators import login_required


def get_next_task(user, plan):

    tasks = plan.tasks.order_by("week_number", "day_number")

    completed_task_ids = UserTaskProgress.objects.filter(
        user=user,
        task__plan=plan,
        completed=True
    ).values_list("task_id", flat=True)

    for task in tasks:
        if task.id not in completed_task_ids:
            return task

    return None

@login_required
def plan_detail(request, plan_id):

    plan = get_object_or_404(ReadingPlan, id=plan_id)

    tasks = plan.tasks.all()

    weeks = {}

    for task in tasks:
        weeks.setdefault(task.week_number, []).append(task)

    completed_ids = UserTaskProgress.objects.filter(
        user=request.user,
        task__plan=plan,
        completed=True
    ).values_list("task_id", flat=True)

    next_task = get_next_task(request.user, plan)

    next_task_id = None
    next_week = None

    if next_task:
        next_task_id = next_task.id
        next_week = next_task.week_number

    total_tasks = tasks.count()
    completed_tasks = len(completed_ids)

    progress_percentage = 0

    if total_tasks > 0:
        progress_percentage = int((completed_tasks / total_tasks) * 100)

    return render(
        request,
        "plans/plan_detail.html",
        {
            "plan": plan,
            "weeks": weeks,
            "user_completed_ids": completed_ids,
            "next_task_id": next_task_id,
            "next_week": next_week,
            "progress_percentage": progress_percentage,
        },
    )