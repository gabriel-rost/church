from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from ...models import ReadingPlan, UserTaskProgress


def plan_users(request, plan_id):

    plan = get_object_or_404(ReadingPlan, id=plan_id)

    # usuários que iniciaram
    started_users_ids = (
        UserTaskProgress.objects
        .filter(task__plan=plan)
        .values_list("user_id", flat=True)
        .distinct()
    )

    started_users = User.objects.filter(id__in=started_users_ids)

    # usuários que NÃO iniciaram
    not_started_users = User.objects.exclude(id__in=started_users_ids)

    # usuários que concluíram
    total_tasks = plan.tasks.count()

    completed_users = (
        UserTaskProgress.objects
        .filter(task__plan=plan, completed=True)
        .values("user")
        .annotate(total=Count("id"))
        .filter(total=total_tasks)
    )

    context = {
        "plan": plan,
        "started_users": started_users,
        "not_started_users": not_started_users,
        "completed_users": completed_users,
    }

    return render(request, "plans/plan_users.html", context)