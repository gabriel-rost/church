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
]