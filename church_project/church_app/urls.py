from django.urls import path

from . import views

urlpatterns = [
    path("post_detail/<int:post_id>/", views.post_detail, name="post_detail"),
    path("login", views.login_view, name="login"),
    path("channel/<int:channel_pk>/new_post/", views.create_post, name="create_post"),
    path("channel/<int:channel_pk>/", views.post_list, name="post_list"), # Lista de posts por canal
    path("logout", views.logout_view, name="logout"),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),  # Página inicial após login
    path('', views.home, name='home'),  # Rota raiz direciona para a home
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),  # Rota para adicionar comentário
    path('profile/<str:username>/', views.perfil_view, name='profile'),  # Rota para a página de perfil do usuário
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # Rota para editar um post
    path('attachment/<int:attachment_id>/remove/', views.remove_attachment, name='remove_attachment'),  # Rota para remover um anexo
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Rota para deletar um post
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),  # Rota para editar o perfil do usuário
    path('changelog/', views.changelog_view, name='changelog'),  # Rota para a página de changelog
    path('manage_channels/', views.manage_channels, name='manage_channels'),  # Rota para gerenciar canais
    path('channel/add/', views.add_channel, name='channel/add_channel'),  # Rota para adicionar um novo canal
    path('channel/<int:channel_pk>/delete/', views.delete_channel, name='delete_channel'),  # Rota para deletar um canal
    path('channel/<int:channel_pk>/edit/', views.edit_channel, name='edit_channel'),  # Rota para editar um canal
    path('channel/manage_channel_members/<int:channel_pk>/', views.manage_channel_members, name='manage_channel_members'),  # Rota para gerenciar membros do canal
    path('channel/<int:channel_pk>/feed/', views.channel_feed, name='channel_feed'),  # Rota para o feed do canal
    path('featured_post/<int:post_id>/', views.add_featured_post, name='featured_post'),  # Rota para adicionar post em destaque
    path('channel/<int:channel_pk>/posts/', views.infinite_scroll_post_list, name='infinite_post_list'),  # Rota para lista de posts com infinite scroll
    path('health_check/', views.health_check, name='health_check'),  # Rota para o endpoint de health check
    path('bible/', views.bible_home, name='bible_home'), # Página inicial da Bíblia
    path('bible/<int:book_id>/<int:chapter_number>/', views.read_chapter, name='read_chapter'), # Ler capítulo específico
    path('bible/<int:book_id>/<int:chapter_number>/<int:verse_number_firth>/', views.read_verse, name='read_verse'), # Ler versículo específico
    path('bible/<int:book_id>/<int:chapter_number>/<int:verse_number_firth>/<int:verse_number_second>/', views.read_verse, name='read_verse_range'), # Ler intervalo de versículos
    path('plan/<int:plan_id>/admin/add_task/', views.admin_add_task, name='admin_add_task'), # Adicionar tarefa ao plano de leitura
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/new/', views.create_plan, name='create_plan'),
    path('plans/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('plans/<int:plan_id>/delete/', views.delete_plan, name='delete_plan'),  # Rota para deletar um plano de leitura
    path('plans/<int:plan_id>/week/<int:week_number>/delete/', views.delete_week, name='delete_week'), # Rota para deletar uma semana do plano de leitura
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),  # Rota para deletar uma tarefa do plano de leitura
    path('send_notification/', views.send_notification_view, name='send_notification'),  # Rota para enviar notificação de teste
]