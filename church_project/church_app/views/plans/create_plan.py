from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from ...models import ReadingPlan
from ...forms import ReadingPlanForm

@staff_member_required
def create_plan(request):
    if request.method == 'POST':
        form = ReadingPlanForm(request.POST, request.FILES)
        if form.is_valid():
            new_plan = form.save()
            # Após criar, vai para o detalhe para o moderador lançar as leituras
            return redirect('plan_detail', plan_id=new_plan.id)
    else:
        form = ReadingPlanForm()
    return render(request, 'plans/create_plan.html', {'form': form})