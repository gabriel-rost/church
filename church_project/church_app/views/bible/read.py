from django.shortcuts import render, get_object_or_404
from church_app.models.bible.book import Book, Chapter, Verse

def read_verse(request, book_id, chapter_number, verse_number):
    book = get_object_or_404(Book, id=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
    verse = get_object_or_404(Verse, chapter=chapter, number=verse_number)
    
    context = {
        'book': book,
        'chapter': chapter,
        'verse': verse,
    }
    
    return render(request, 'bible/read_verse.html', context)