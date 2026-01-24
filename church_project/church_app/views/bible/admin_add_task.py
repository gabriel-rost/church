from django.shortcuts import render, redirect
from ...forms import PlanTaskForm
from ...models import ReadingPlan, PlanTask
from church_app.models.bible.book import Chapter

def admin_add_task(request, plan_id):
    plan = ReadingPlan.objects.get(id=plan_id)
    
    if request.method == 'POST':
        form = PlanTaskForm(request.POST)
        if form.is_valid():
            # 1. Salva a tarefa (Semana e Dia)
            task = form.save(commit=False)
            task.plan = plan
            task.save()

            # 2. Busca os capítulos no banco baseado no intervalo escolhido
            book = form.cleaned_data['book']
            start = form.cleaned_data['start_chapter']
            end = form.cleaned_data['end_chapter']
            
            chapters = Chapter.objects.filter(
                book=book, 
                number__range=(start, end)
            )

            # 3. Associa os capítulos à tarefa (ManyToMany)
            task.chapters.set(chapters)
            
            return redirect('plan_detail', plan_id=plan.id)
    else:
        form = PlanTaskForm()

    return render(request, 'plans/admin_add_task.html', {'form': form, 'plan': plan})