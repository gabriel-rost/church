from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="post_list"),
    path("<int:post_id>/", views.post, name="post_detail"),
    path("login", views.login_view, name="login"),
]