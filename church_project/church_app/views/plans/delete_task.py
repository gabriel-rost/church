from django.contrib.auth.decorators import permission_required

@permission_required('church_app.can_edit_reading_plan', raise_exception=True)
def delete_task(request, task_id):
    from django.shortcuts import get_object_or_404, redirect
    from church_app.models.bible.plantask import PlanTask
    from django.contrib.auth.decorators import login_required
    from django.core.exceptions import PermissionDenied

    task = get_object_or_404(PlanTask, id=task_id)
    plan_id = task.plan.id
    task.delete()
    return redirect('plan_detail', plan_id=plan_id)