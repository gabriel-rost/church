from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Post
from django.db import transaction
from .forms import ContentForm
from .models import Channel, Post, Archive
from django.contrib.auth.decorators import login_required # Garante que o usuário esteja logado
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from .forms import SignUpForm

# Create your views here.

@staff_member_required
def index(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "church_app/post_list.html", {"posts": posts})

@login_required
def home(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "church_app/post_list.html", {"posts": posts})

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
    return HttpResponse("Logout successful")

@login_required
@transaction.atomic # Garante que tudo seja salvo ou nada seja salvo
def create_post(request, channel_pk):
    # 1. Obtém o canal (ex: via URL)
    channel = get_object_or_404(Channel, pk=channel_pk)
    
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
