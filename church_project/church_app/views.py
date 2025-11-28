import os
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Post
from django.db import transaction
from .forms import ContentForm
from .models import Channel, Post, Archive, User
from django.contrib.auth.decorators import login_required # Garante que o usuário esteja logado
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from .forms import SignUpForm
from django.contrib import messages # Para feedback visual ao usuário
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    channels = Channel.objects.all()
    return render(request, "home.html", {"channels": channels})

@login_required
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # comentários principais (parent = None)
    comments = post.comments.filter(parent__isnull=True)
    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments
    })

@login_required
def post_list(request, channel_pk):
    channel = get_object_or_404(Channel, pk=channel_pk)
    posts = channel.posts.all().order_by("-date")

    if request.user not in channel.members.all():
        return HttpResponse("Você não tem permissão para ver os posts deste canal.", status=403)

    return render(request, "church_app/post_list.html", {
        "posts": posts,
        "channel": channel
    })

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        return HttpResponse("Login successful")
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponse("<script>alert('Logout successful'); window.location='/login';</script>")

@login_required
@transaction.atomic # Garante que tudo seja salvo ou nada seja salvo
def create_post(request, channel_pk):
    # 1. Obtém o canal (ex: via URL)
    channel = get_object_or_404(Channel, pk=channel_pk)

    if request.user not in channel.members.all():
        return HttpResponse("Você não tem permissão para postar neste canal.", status=403)
    
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
            
            # Sucesso! Redireciona para o novo post
            return redirect('post_detail', post_id=new_post.pk) 
    
    else:
        # Requisição GET: Exibe o formulário vazio
        form = ContentForm()
        
    context = {
        'form': form,
        'channel': channel,
    }
    return render(request, 'create_post.html', context)

@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Perfil é criado automaticamente via signals
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        parent_id = request.POST.get('commentId')

        if not text:
            return redirect('post_detail', post_id=post_id)

        if parent_id:  # é uma resposta
            parent_comment = post.comments.filter(id=parent_id).first()
            if parent_comment:
                post.comments.create(user=request.user, text=text, parent=parent_comment)
        else:  # é um comentário principal
            post.comments.create(user=request.user, text=text)

    return redirect('post_detail', post_id=post_id)

@login_required
def perfil_view(request, username):
    if request.user.username != username:
        return HttpResponse("Você não tem permissão para ver este perfil.", status=403)
    return render(request, "profile/user_profile.html")

@login_required
@transaction.atomic
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    content = post.content  # conteúdo relacionado ao post
    
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        uploaded_files = request.FILES.getlist('attachments')

        if form.is_valid():
            content = form.save()

            # 🔹 Adicionar novos arquivos
            new_archives = []
            for uploaded_file in uploaded_files:
                archive = Archive.objects.create(file=uploaded_file)
                new_archives.append(archive)

            # Mantém os arquivos antigos + novos
            content.attachments.add(*new_archives)

            # Se o usuário clicar em "Salvar", não apaga nada ainda
            # (A exclusão pode ser feita em um form separado)
            return redirect('post_detail', post_id=post.pk)
    else:
        form = ContentForm(instance=content)

    # 🔹 Lista atual de anexos
    archive = content.attachments.all()

    context = {
        'form': form,
        'post': post,
        'archive': archive
    }
    return render(request, 'post/edit_post.html', context)

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

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST' and request.user == post.user:
        channel_pk = post.channel.pk
        post.delete()
        return redirect('post_list', channel_pk=channel_pk)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# @login_required
# @transaction.atomic
# def edit_user_profile(request):
#     profile = request.user.profile

#     if request.method == 'POST':
#         from .forms import ProfileForm  # Importa aqui para evitar importação circular
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('perfil', username=request.user.username)
#     else:
#         from .forms import ProfileForm
#         form = ProfileForm(instance=profile)

#     return render(request, 'profile/edit_user_profile.html', {'form': form})

def edit_user_profile(request):
    from .forms import ProfileForm, UserForm  # Importa aqui para evitar importação circular
    profile = request.user.profile

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('perfil', username=request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form
    }
    return render(request, 'profile/edit_user_profile.html', context)


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

@staff_member_required
def manage_channels(request):
    channels = Channel.objects.all()
    return render(request, 'manage_channels.html', {'channels': channels})

@staff_member_required
def add_channel(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            Channel.objects.create(name=name)
            return redirect('manage_channels')

    return render(request, 'channel/add_channel.html')

@staff_member_required
def delete_channel(request, channel_pk):
    if request.method == 'POST':
        channel = get_object_or_404(Channel, pk=channel_pk)
        channel.posts.all().delete()  # Deleta todos os posts associados ao canal
        channel.delete()
        return redirect('manage_channels')
    return HttpResponse("Método não permitido", status=405)

@staff_member_required
def edit_channel(request, channel_pk):
    all_users = User.objects.all()
    channel = get_object_or_404(Channel, pk=channel_pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        members_ids = request.POST.getlist('members')
        channel.members.set(members_ids)
        #description = request.POST.get('description', '')

        if name:
            channel.name = name
            #channel.description = description
            channel.save()
            return redirect('manage_channels')

    context = {
        'all_users': all_users,
        'channel': channel
    }
    return render(request, 'channel/edit_channel.html', context)

@staff_member_required
def manage_channel_members(request, channel_pk):
    channel = get_object_or_404(Channel, pk=channel_pk)
    
    # Busca todos os usuários, exceto os que JÁ ESTÃO no canal
    # (Otimização: use o ORM para filtrar)
    channel_members_pks = channel.members.values_list('pk', flat=True)
    non_members = User.objects.exclude(pk__in=channel_members_pks).all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user_to_manage = get_object_or_404(User, pk=user_id)
        
        if action == 'add':
            channel.members.add(user_to_manage)
        elif action == 'remove':
            channel.members.remove(user_to_manage)
        
        # Redireciona para evitar re-submissão do formulário
        return redirect('manage_channel_members', channel_pk=channel_pk)

    context = {
        'channel': channel,
        # O Django fornece channel.members.all automaticamente
        'non_members': non_members,
    }
    return render(request, 'channel/manage_channel_members.html', context)