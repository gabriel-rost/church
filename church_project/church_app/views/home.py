from django.shortcuts import render
from ..models import Channel, FeaturedPost, Post, ActivityLog
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    """
    View principal (Dashboard) que segmenta a experiência entre liderança e membros.
    
    Esta view atua como um hub central. Se o usuário possuir a permissão 
    :attr:`church_app.can_approve_waitlist`, ela injeta métricas de gestão. 
    Caso contrário (ou adicionalmente), renderiza o feed de conteúdo.

    Args:
        request (HttpRequest): Objeto de requisição padrão do Django.

    Context Variables:
        - Para Administradores (:class:`User` com permissão):
            - `pending_count` (int): Total de :class:`User` com `is_approved=False`.
            - `moderators_count` (int): Total de usuários no :class:`Group` 'Moderador'.
            - `recent_logs` (QuerySet): Os 3 registros mais recentes de :class:`ActivityLog`.
        
        - Para Todos os Usuários:
            - `channels` (QuerySet): Lista de todos os :class:`Channel`.
            - `featured_posts` (QuerySet): O registro mais recente de :class:`FeaturedPost`.
            - `posts` (QuerySet): Os 3 últimos objetos de :class:`Post`.

    Returns:
        HttpResponse: Renderiza o template 'home.html'.
    """
    context = {}
    
    # 1. Lógica de Gestão (Visível apenas para Liderança/Moderadores)
    if request.user.is_authenticated and request.user.has_perm('church_app.can_approve_waitlist'):
        context['pending_count'] = User.objects.filter(is_approved=False).count()
        context['moderators_count'] = User.objects.filter(groups__name='Moderador').count()
        context['recent_logs'] = ActivityLog.objects.all()[:3]
    
    # 2. Lógica de Conteúdo (Visível para todos os membros aprovados)
    context['channels'] = Channel.objects.all()
    context['featured_posts'] = FeaturedPost.objects.order_by('-id')[:1]
    context['posts'] = Post.objects.order_by('-date')[:3]
    
    return render(request, "home.html", context)