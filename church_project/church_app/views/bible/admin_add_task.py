from django.shortcuts import render, redirect
from ...forms import PlanTaskForm
from ...models import ReadingPlan, PlanTask, Archive
from church_app.models.bible.book import Chapter

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def admin_add_task(request, plan_id):
    plan = get_object_or_404(ReadingPlan, id=plan_id)

    if request.method == 'POST':
        form = PlanTaskForm(request.POST, request.FILES)

        if form.is_valid():
            print("VALIDOU")
            task = form.save(commit=False)
            task.plan = plan

            # Upload de arquivo (antes de salvar definitivamente)
            if request.FILES.get('file'):
                task.file = request.FILES['file']

            task.save()

            # 📚 Capítulos
            book = form.cleaned_data['book']
            start = form.cleaned_data['start_chapter']
            end = form.cleaned_data['end_chapter']

            chapters = Chapter.objects.filter(
                book=book,
                number__range=(start, end)
            ).order_by('number')

            task.chapters.set(chapters)

            messages.success(request, "Leitura adicionada com sucesso!")
            return redirect('plan_detail', plan_id=plan.id)

        else:
            print("ERROS:", form.errors)
            messages.error(request, "Erro ao salvar. Verifique os campos.")

    else:
        form = PlanTaskForm()

    return render(
        request,
        'plans/admin_add_task.html',
        {
            'form': form,
            'plan': plan
        }
    )


from django.http import JsonResponse
from ...models import Chapter, Verse

def get_chapters(request):
    book_id = request.GET.get('book_id')

    chapters = Chapter.objects.filter(book_id=book_id).order_by('number')

    data = [
        {"id": c.id, "number": c.number}
        for c in chapters
    ]

    return JsonResponse(data, safe=False)


def get_verse_count(request):
    chapter_id = request.GET.get('chapter_id')

    count = Verse.objects.filter(chapter_id=chapter_id).count()

    return JsonResponse({'count': count})