from django.shortcuts import render, get_object_or_404
from church_app.models.bible.book import Book, Chapter, Verse

def read_verse(request, book_id, chapter_number, verse_number_firth, verse_number_second=0):
    
    book = get_object_or_404(Book, id=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)

    if verse_number_second == 0 or verse_number_second is None:
        # Ex.: Genesis 1:1
        verse = get_object_or_404(Verse, chapter=chapter, number=verse_number_firth)

        context = {
            'book': book,
            'chapter': chapter,
            'verse': verse,
            'verses': None,
        }
        
        return render(request, 'bible/read_verse.html', context)

    # Ex.: Genesis 1:1-2
    verses = Verse.objects.filter(chapter=chapter, number__gte=verse_number_firth, number__lte=verse_number_second)

    print(verses.values())

    context = {
        'book': book,
        'chapter': chapter,
        'verses': verses,
    }
    
    return render(request, 'bible/read_verse.html', context)