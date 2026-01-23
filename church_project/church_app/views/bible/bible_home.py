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