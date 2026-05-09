from django.shortcuts import render, get_object_or_404
from collections import defaultdict
from django.utils import timezone
from django.utils.timezone import localdate

from ...models import ReadingPlan, UserTaskProgress, Post
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


from django.utils import timezone

def get_next_task(user, plan):

    tasks = plan.tasks.order_by("scheduled_date")

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

    # Permissão para plano rascunho
    if not plan.is_published:
        if not request.user.has_perm('church_app.can_edit_reading_plan'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Você não tem permissão para visualizar este plano rascunho.")

    # Post relacionado
    plan_type = ContentType.objects.get_for_model(plan)
    related_post = Post.objects.filter(
        content_type=plan_type,
        object_id=plan.id
    ).first()

    tasks = plan.tasks.all().order_by("scheduled_date")

    grouped_tasks = defaultdict(list)

    for task in tasks:
        if task.scheduled_date:
            date_key = task.scheduled_date
        else:
            date_key = None

        grouped_tasks[date_key].append(task)

    grouped_tasks = dict(grouped_tasks)

    # progresso do usuário
    completed_ids = set(UserTaskProgress.objects.filter(
        user=request.user,
        task__plan=plan,
        completed=True
    ).values_list("task_id", flat=True))

    next_task = get_next_task(request.user, plan)

    next_task_id = next_task.id if next_task else None

    # progresso
    total_tasks = tasks.count()
    completed_tasks = len(completed_ids)

    progress_percentage = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render(
        request,
        "plans/plan_detail.html",
        {
            "plan": plan,
            "grouped_tasks": grouped_tasks,
            "tasks": tasks,  # útil se quiser lista simples
            "user_completed_ids": completed_ids,
            "next_task_id": next_task_id,
            "progress_percentage": progress_percentage,
            "related_post": related_post,
            "today": localdate(),
            "now": timezone.now(),
        },
    )