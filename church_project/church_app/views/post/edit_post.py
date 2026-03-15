from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from church_app.models import Post, Archive
from church_app.forms import PostForm

@login_required
@transaction.atomic
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    #content = post.content  # conteúdo relacionado ao post
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        uploaded_files = request.FILES.getlist('attachments')

        if form.is_valid():
            post = form.save()

            # 🔹 Adicionar novos arquivos
            new_archives = []
            for uploaded_file in uploaded_files:
                archive = Archive.objects.create(file=uploaded_file)
                new_archives.append(archive)

            # Mantém os arquivos antigos + novos
            post.attachments.add(*new_archives)

            # Se o usuário clicar em "Salvar", não apaga nada ainda
            # (A exclusão pode ser feita em um form separado)
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)

    # 🔹 Lista atual de anexos
    archive = post.attachments.all()

    context = {
        'form': form,
        'post': post,
        'archive': archive
    }
    return render(request, 'post/edit_post.html', context)