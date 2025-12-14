from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from church_app.models import Archive
from django.contrib import messages

@login_required
@transaction.atomic
def remove_attachment(request, attachment_id):
    # Garante que a deleção ocorra apenas via POST
    if request.method == 'POST':
        attachment = get_object_or_404(Archive, pk=attachment_id)
        
        try:
            # 1. Remove o arquivo do Cloudflare R2
            attachment.file.delete(save=False)
            
            # 2. Remove o registro do PostgreSQL
            attachment.delete()
            
            # Adiciona uma mensagem de sucesso para o usuário
            messages.success(request, f"Anexo '{attachment.filename}' removido com sucesso.")

        except Exception as e:
            # Em caso de falha de deleção do R2 ou do banco
            messages.error(request, f"Erro ao remover anexo: {e}")
        
        # 3. Redireciona para a página anterior (HTTP_REFERER)
        # Se o HTTP_REFERER não existir (por segurança), redireciona para uma URL segura (ex: lista de posts)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
        
    # Se o método não for POST (o que não deve acontecer pelo seu formulário), retorna 405
    return HttpResponse("Método não permitido", status=405)