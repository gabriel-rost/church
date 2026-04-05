from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from church_app.models import Post
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def search_homepage(request):
    return render(request, "search/search_homepage.html")

import re
from django.db.models import Q
from django.core.paginator import Paginator
from church_app.models.bible.book import Verse, Book

@login_required
def search_results(request):
    query_text = request.GET.get("q", "").strip()
    filter_type = request.GET.get("filter", "all")
    
    posts = []
    users = []
    bible_verses = Verse.objects.none()

    if query_text:
        # --- 1. LÓGICA DA BÍBLIA (Onde o FTS costuma falhar) ---
        if filter_type in ['all', 'bible']:
            # Tentamos primeiro ver se é uma referência (ex: João 3:16 ou João 3)
            # Regex: (Nome do Livro) (Capítulo) (opcional :Versículo)
            match = re.match(r'^([\d\s]*[a-zA-Záàâãéèêíïóôõöúçñ]+)\s+(\d+)(?:[:\s](\d+))?$', query_text)
            
            if match:
                book_name = match.group(1).strip()
                cap_num = match.group(2)
                verse_num = match.group(3)
                
                # Busca o livro. Usamos icontains para "Joao" achar "João"
                book = Book.objects.filter(name__icontains=book_name).first()
                if book:
                    lookup = Q(chapter__book=book, chapter__number=cap_num)
                    if verse_num:
                        lookup &= Q(number=verse_num)
                    
                    bible_verses = Verse.objects.filter(lookup).select_related('chapter__book')

            # Se NÃO foi uma referência ou a busca por ref não trouxe nada, buscamos pelo TEXTO
            if not bible_verses.exists():
                bible_verses = Verse.objects.filter(
                    text__icontains=query_text
                ).select_related('chapter__book')[:20]

        # --- 2. BUSCA EM POSTS (Usando icontains para frases exatas) ---
        if filter_type in ['all', 'posts']:
            posts_qs = Post.objects.filter(
                Q(title__icontains=query_text) | 
                Q(text__icontains=query_text)
            ).order_by("-date")
            
            paginator = Paginator(posts_qs, 5)
            posts = paginator.get_page(request.GET.get("page"))

        # --- 3. BUSCA EM USUÁRIOS ---
        if filter_type in ['all', 'users']:
            users = User.objects.filter(
                Q(username__icontains=query_text) | 
                Q(first_name__icontains=query_text) |
                Q(last_name__icontains=query_text)
            ).distinct()[:10]

    return render(request, "search/search_results.html", {
        "query": query_text,
        "posts": posts,
        "users": users,
        "bible_verses": bible_verses,
        "filter_type": filter_type
    })