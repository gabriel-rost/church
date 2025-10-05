from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="post_list"),
    path("post_detail/<int:post_id>/", views.post, name="post_detail"),
    path("login", views.login_view, name="login"),
    path("channel/<int:channel_pk>/new_post/", views.create_post, name="create_post"),
    path("channel/<int:channel_pk>/", views.post_list, name="post_list"), # Lista de posts por canal
    path("logout", views.logout_view, name="logout"),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),  # Página inicial após login
]