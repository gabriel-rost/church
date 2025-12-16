from django.shortcuts import render
import os

def changelog_view(request):
    # 1. Definir o caminho absoluto ou relativo para o arquivo
    # É melhor usar o caminho absoluto para evitar problemas de execução.
    # Exemplo: O arquivo está em uma pasta 'docs' dentro do seu app
    # CUIDADO: Ajuste 'my_app' e 'docs/content.md' para o seu caminho real.
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Ajuste conforme necessário
    markdown_path = os.path.join(base_dir,'./../../', 'CHANGELOG.md')
    print(markdown_path)
    
    markdown_content = None

    try:
        # 2. Abrir e ler o conteúdo do arquivo
        with open(markdown_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
    except FileNotFoundError:
        markdown_content = "Erro: O arquivo Markdown não foi encontrado."
    except Exception as e:
        markdown_content = f"Erro ao carregar o arquivo: {e}"

    context = {
        'markdown_text': markdown_content,
    }
    return render(request, 'changelog.html', context)