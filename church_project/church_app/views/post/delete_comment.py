from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from ...models import Comment
from ...models.activity_log import log_activity

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id

    # Verifica se o método é POST e se o usuário tem autoridade
    if request.method == 'POST':
        is_owner = request.user == comment.user
        has_permission = request.user.has_perm('app_label.can_delete_comment')

        if is_owner:
            comment.delete()
            messages.success(request, "Comentário excluído com sucesso!")
        
        elif has_permission:
            comment.delete()
            log_activity(request.user, f"{request.user} ocultou comentário de {comment.user} em {comment.post}", comment)
            print(f"{request.user} ocultou comentário de {comment.user} em {comment.post}")
            messages.success(request, "Comentário excluído com sucesso!")

        else:
            messages.error(request, "Você não tem permissão para excluir este comentário.")
    
    # Redireciona de volta para a página do post (ajuste o nome da rota conforme seu projeto)
    return redirect('post_detail', post_id=post_id)