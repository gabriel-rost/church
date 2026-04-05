from django.shortcuts import render
from church_app.models.bible.book import Book

def bible_home(request):
    books = Book.objects.all().order_by('order')
    
    # Separando por Antigo e Novo Testamento (Opcional, mas ajuda a UX)
    # Livros 1 a 39 = Antigo / 40 a 66 = Novo
    old_testament = books.filter(order__lte=39)
    new_testament = books.filter(order__gt=39)

    return render(request, 'bible/index.html', {
        'old_testament': old_testament,
        'new_testament': new_testament,
    })

from django.http import JsonResponse
from ...models import Verse, Chapter # Certifique-se de importar Chapter se necessário

def get_chapters(request, book_id):
    # O Django usa o sufixo __ para buscar em campos relacionados
    # Aqui buscamos todos os capítulos que pertencem ao book_id informado
    chapters_count = Chapter.objects.filter(book_id=book_id).count()
    
    # Se você não tiver o modelo Chapter separado e tudo estiver em Verse, 
    # você usaria: Verse.objects.filter(chapter__book_id=book_id)...
    
    return JsonResponse({'chapters': chapters_count})

def get_verses_count(request, book_id, chapter):
    # Filtramos os versículos que pertencem ao capítulo X do livro Y
    # Usamos chapter__number (ou o campo que guarda o número do cap) e chapter__book_id
    verses_count = Verse.objects.filter(
        chapter__book_id=book_id, 
        chapter__number=chapter
    ).count()
    
    return JsonResponse({'verses': verses_count})