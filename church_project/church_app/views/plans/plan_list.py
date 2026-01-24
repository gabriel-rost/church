from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from ...models import ReadingPlan
from ...forms import ReadingPlanForm

def plan_list(request):
    plans = ReadingPlan.objects.all().order_by('-created_at')
    return render(request, 'plans/plan_list.html', {'plans': plans})