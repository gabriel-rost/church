from django.shortcuts import render, get_object_or_404
from church_app.models.bible.book import Book, Chapter

def read_chapter(request, book_id, chapter_number):
    # Carrega o livro e o capítulo específico
    book = get_object_or_404(Book, id=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
    
    # Busca todos os versículos daquele capítulo ordenados
    verses = chapter.verses.all().order_by('number')
    
    # Lógica simples para botões Próximo/Anterior
    prev_chapter = book.chapters.filter(number=chapter_number - 1).first()
    next_chapter = book.chapters.filter(number=chapter_number + 1).first()

    context = {
        'book': book,
        'chapter': chapter,
        'verses': verses,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    }
    
    return render(request, 'bible/read_chapter.html', context)