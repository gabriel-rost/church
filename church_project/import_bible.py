import os
import json
import django
from django.utils.text import slugify

# 1. Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church_site.settings') # Ajuste para o nome do seu projeto
django.setup()

from church_app.models.bible.book import Book, Chapter, Verse

def run_import():
    file_path = 'bible.json'
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado na raiz do projeto.")
        return

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    print(f"Iniciando importação de {len(data)} livros...")

    for i, book_data in enumerate(data, 1):
        # Criar ou pegar o Livro
        book_name = book_data['name']
        book, created = Book.objects.get_or_create(
            name=book_name,
            defaults={'order': i}
        )
        
        if not created:
            print(f"Pulando {book_name} (já existe no banco).")
            continue

        print(f"Importando: {book_name}...")

        for c_idx, chapter_verses in enumerate(book_data['chapters'], 1):
            # Criar o Capítulo
            chapter = Chapter.objects.create(book=book, number=c_idx)
            
            # Preparar Versículos para inserção em massa (Bulk Create)
            verses_to_create = []
            for v_idx, text in enumerate(chapter_verses, 1):
                verses_to_create.append(
                    Verse(chapter=chapter, number=v_idx, text=text)
                )
            
            # Inserção ultra rápida no Postgres
            Verse.objects.bulk_create(verses_to_create)

    print("\n✅ Importação concluída com sucesso!")

if __name__ == "__main__":
    run_import()