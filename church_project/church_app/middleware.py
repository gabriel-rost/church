from django.shortcuts import redirect
from django.urls import reverse

class GlobalAppMiddleware:
    """
    Middleware de Gestão de Fluxo Global.
    
    Responsabilidades:
    1. Forçar autenticação em rotas privadas (Gatekeeper).
    2. Gerenciar o funil de aprovação de novos usuários (Waitlist).
    3. Garantir acesso irrestrito para administradores (Staff).
    
    Performance: Utiliza busca em conjuntos (sets) O(1) para minimizar o impacto 
    no tempo de resposta por requisição.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user = request.user

        # ---------------------------------------------------------------------
        # 1. VALIDAÇÃO DE USUÁRIOS ANÔNIMOS (GATEKEEPER)
        # ---------------------------------------------------------------------
        if not user.is_authenticated:
            # URLs que podem ser acessadas sem login (Whitelist Pública)
            public_paths = {
                reverse('login'),
                reverse('signup'),
                reverse('password_reset'),
                reverse('password_reset_done'),
                reverse('password_reset_complete'),
            }

            # Verifica se o caminho atual não é público e não é uma rota de confirmação de senha
            if path not in public_paths and not path.startswith('/reset/'):
                return redirect('login')
            
            # Se for anônimo e estiver em rota pública, segue o fluxo
            return self.get_response(request)

        # ---------------------------------------------------------------------
        # 2. VALIDAÇÃO DE USUÁRIOS LOGADOS
        # ---------------------------------------------------------------------
        
        # Bypass imediato para Administradores: Performance e Segurança
        if user.is_staff:
            return self.get_response(request)

        # Controle de Aprovação (Comunidade)
        # Usuários logados mas ainda não aprovados pela administração
        if not getattr(user, 'is_approved', False):
            # URLs permitidas para usuários em "quarentena"
            allowed_internal_paths = {
                reverse('waitlist_status'), 
                reverse('logout'),
            }

            if path not in allowed_internal_paths:
                return redirect('waitlist_status')

        # Se passou por todos os filtros, libera a requisição
        return self.get_response(request)