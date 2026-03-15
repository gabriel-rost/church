from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from ...models import ReadingPlan, UserTaskProgress


def community_plan_dashboard(request, plan_id):

    plan = get_object_or_404(ReadingPlan, id=plan_id)

    total_tasks = plan.tasks.count()

    # 👥 usuários que iniciaram
    users_started = (
        UserTaskProgress.objects
        .filter(task__plan=plan)
        .values("user")
        .distinct()
        .count()
    )

    # 🔥 ativos últimos 7 dias
    last_week = timezone.now() - timedelta(days=7)

    active_users = (
        UserTaskProgress.objects
        .filter(
            task__plan=plan,
            completed=True,
            completed_at__gte=last_week
        )
        .values("user")
        .distinct()
        .count()
    )

    # 🏁 usuários que completaram o plano
    completed_users = (
        UserTaskProgress.objects
        .filter(task__plan=plan, completed=True)
        .values("user")
        .annotate(total=Count("id"))
        .filter(total=total_tasks)
        .count()
    )

    # 📈 progresso médio
    total_completed = (
        UserTaskProgress.objects
        .filter(task__plan=plan, completed=True)
        .count()
    )

    if users_started > 0 and total_tasks > 0:
        progress_percentage = int(
            total_completed / (users_started * total_tasks) * 100
        )
    else:
        progress_percentage = 0

    # 🏆 ranking
    ranking = (
        UserTaskProgress.objects
        .filter(task__plan=plan, completed=True)
        .values("user__username")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    # 📖 atividade recente
    recent_activity = (
        UserTaskProgress.objects
        .filter(task__plan=plan, completed=True)
        .select_related("user", "task")
        .order_by("-completed_at")[:10]
    )

    # 📊 leituras populares
    popular_tasks = (
        UserTaskProgress.objects
        .filter(task__plan=plan, completed=True)
        .values("task__day_number")
        .annotate(total=Count("id"))
        .order_by("-total")[:10]
    )

    context = {
        "plan": plan,
        "users_started": users_started,
        "active_users": active_users,
        "completed_users": completed_users,
        "progress_percentage": progress_percentage,
        "ranking": ranking,
        "recent_activity": recent_activity,
        "popular_tasks": popular_tasks,
    }

    return render(request, "community/plan_dashboard.html", context)