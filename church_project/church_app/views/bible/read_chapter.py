from django.shortcuts import render, get_object_or_404
from church_app.models.bible.book import Book, Chapter

def read_chapter(request, book_id, chapter_number):
    book = get_object_or_404(Book, id=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
    
    verses = chapter.verses.all().order_by('number')
    all_chapters = book.chapters.all().order_by('number')
    
    # Navegação dentro do livro atual
    prev_chapter = book.chapters.filter(number=chapter_number - 1).first()
    next_chapter = book.chapters.filter(number=chapter_number + 1).first()

    # Lógica para Transição de Livro (Caso não haja próximo capítulo)
    next_book = None
    prev_book = None
    
    if not next_chapter:
        # Busca o próximo livro na sequência (Ex: de Mateus para Marcos)
        next_book = Book.objects.filter(order__gt=book.order).order_by('order').first()
        
    if not prev_chapter:
        # Busca o livro anterior (Ex: de Marcos para Mateus)
        prev_book = Book.objects.filter(order__lt=book.order).order_by('-order').first()

    context = {
        'book': book,
        'chapter': chapter,
        'verses': verses,
        'all_chapters': all_chapters,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'next_book': next_book,  # Passamos o próximo livro
        'prev_book': prev_book,  # Passamos o livro anterior
    }
    
    return render(request, 'bible/read_chapter.html', context)