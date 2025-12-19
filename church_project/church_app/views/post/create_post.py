from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from church_app.models import Channel, Post, Archive
from church_app.forms import ContentForm
from django.http import HttpResponseForbidden

@login_required
@transaction.atomic # Garante que tudo seja salvo ou nada seja salvo
def create_post(request, channel_pk):
    # 1. Obtém o canal (ex: via URL)
    channel = get_object_or_404(Channel, pk=channel_pk)

    if not channel.members.filter(pk=request.user.pk).exists() and channel.public == False:
            return HttpResponseForbidden("Você não tem permissão para postar neste canal.")
    
    if request.method == 'POST':
        # Instancia o ContentForm com os dados de texto
        form = ContentForm(request.POST) 
        
        # O Django trata uploads em 'request.FILES' (diferente de 'request.POST')
        uploaded_files = request.FILES.getlist('attachments') 
        
        if form.is_valid():
            # 2. Salva o Content primeiro
            content = form.save()
            
            # 3. Cria o objeto Post
            new_post = Post.objects.create(
                user=request.user,
                channel=channel,
                content=content  # Associa o Content que acabamos de salvar
                # 'date' é auto_now_add=True, então será preenchido automaticamente
            )
            
            # 4. Processa e associa os arquivos
            archive_objects = []
            for uploaded_file in uploaded_files:
                # Cria e salva o objeto Archive para cada arquivo
                archive = Archive.objects.create(file=uploaded_file)
                archive_objects.append(archive)
            
            # 5. Adiciona os objetos Archive ao campo ManyToMany do Content
            content.attachments.set(archive_objects) 

            # Sucesso! Redireciona para a lista de posts do canal
            return redirect('post_list', channel_pk=channel.pk)

    else:
        # Requisição GET: Exibe o formulário vazio
        form = ContentForm()
        
    context = {
        'form': form,
        'channel': channel,
    }
    return render(request, 'create_post.html', context)