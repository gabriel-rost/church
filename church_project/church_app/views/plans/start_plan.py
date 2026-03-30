from ...models import ReadingPlan, UserPlanProgress, UserTaskProgress, PlanTask
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def start_plan(request, plan_id):

    plan = get_object_or_404(ReadingPlan, id=plan_id)

    plan_progress, created = UserPlanProgress.objects.get_or_create(
        user=request.user,
        plan=plan
    )

    if created:
        tasks = plan.tasks.all()

        for task in tasks:
            UserTaskProgress.objects.get_or_create(
                user=request.user,
                task=task
            )

    return redirect("plan_detail", plan_id=plan.id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

@login_required
def complete_task(request, task_id):

    task = get_object_or_404(PlanTask, id=task_id)

    progress, created = UserTaskProgress.objects.get_or_create(
        user=request.user,
        task=task
    )

    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

    return redirect("plan_detail", plan_id=task.plan.id)

@login_required
def plan_progress(request, plan_id):

    plan = get_object_or_404(ReadingPlan, id=plan_id)

    total_tasks = plan.tasks.count()

    completed_tasks = UserTaskProgress.objects.filter(
        user=request.user,
        task__plan=plan,
        completed=True
    ).count()

    progress_percentage = 0

    if total_tasks > 0:
        progress_percentage = int((completed_tasks / total_tasks) * 100)

    return render(
        request,
        "plans/plan_progress.html",
        {
            "plan": plan,
            "progress_percentage": progress_percentage
        }
    )

## Funcao auxiliar para listar proxima leitura
def get_next_task(user, plan):

    tasks = plan.tasks.order_by("week_number", "day_number")

    for task in tasks:

        progress = UserTaskProgress.objects.filter(
            user=user,
            task=task,
            completed=True
        ).exists()

        if not progress:
            return task

    return None

@login_required
def continue_plan(request, plan_id):

    plan = get_object_or_404(ReadingPlan, id=plan_id)

    next_task = get_next_task(request.user, plan)

    if not next_task:
        return redirect("plan_detail", plan_id=plan.id)

    first_chapter = next_task.chapters.first()

    if not first_chapter:
        return redirect("plan_detail", plan_id=plan.id)

    if next_task.start_verse:
        return redirect(
            "read_verse_range",
            first_chapter.book.id,
            first_chapter.number,
            next_task.start_verse,
            next_task.end_verse
        )

    return redirect(
        "read_chapter",
        first_chapter.book.id,
        first_chapter.number
    )