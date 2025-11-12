from django.urls import path

from . import views

urlpatterns = [
    path("post_detail/<int:post_id>/", views.post, name="post_detail"),
    path("login", views.login_view, name="login"),
    path("channel/<int:channel_pk>/new_post/", views.create_post, name="create_post"),
    path("channel/<int:channel_pk>/", views.post_list, name="post_list"), # Lista de posts por canal
    path("logout", views.logout_view, name="logout"),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),  # Página inicial após login
    path('', views.home, name='home'),  # Rota raiz direciona para a home
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),  # Rota para adicionar comentário
    path('perfil/<str:username>/', views.perfil_view, name='perfil'),  # Rota para a página de perfil do usuário
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # Rota para editar um post
    path('attachment/<int:attachment_id>/remove/', views.remove_attachment, name='remove_attachment'),  # Rota para remover um anexo
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Rota para deletar um post
    path('profile/edit/', views.edit_user_profile, name='edit_user_profile'),  # Rota para editar o perfil do usuário
]