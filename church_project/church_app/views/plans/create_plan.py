from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from ...models import ReadingPlan
from ...forms import ReadingPlanForm
from django.contrib.auth import get_user_model
User = get_user_model()

@permission_required('church_app.can_create_reading_plan', raise_exception=True)
def create_plan(request):
    if request.method == 'POST':
        form = ReadingPlanForm(request.POST, request.FILES)
        if form.is_valid():
            new_plan = form.save(commit=False)
            
            new_plan.author = request.user
            
            new_plan.save()

            if new_plan.is_published:
                from ...services.notifications import trigger_notifications # Import local para evitar circularidade
                users = User.objects.filter(is_active=True)
                trigger_notifications(users, new_plan)

            return redirect('plan_detail', plan_id=new_plan.id)
    else:
        form = ReadingPlanForm()
    return render(request, 'plans/create_plan.html', {'form': form})