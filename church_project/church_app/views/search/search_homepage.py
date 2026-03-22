from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator
from church_app.models import Post
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def search_homepage(request):
    return render(request, "search/search_homepage.html")

@login_required
def search_results(request):
    query = request.GET.get("q", "").strip()
    filters = request.GET.getlist("filter")

    posts = Post.objects.none()
    users = User.objects.none()

    if not query:
        return render(
            request,
            "search/search_results.html",
            {"query": query, "posts": posts, "users": users},
        )

    # queryset base de posts
    posts_qs = (
            # Removed .select_related("post") as it's self-referential and invalid here
            Post.objects.filter(
                Q(title__icontains=query) |
                Q(text__icontains=query)
            )
            .annotate(
                relevance=Case(
                    When(title__icontains=query, then=2),
                    When(text__icontains=query, then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            .order_by("-relevance")
            .distinct()
        )

    # usuários
    users_qs = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )

    # ===== PAGINAÇÃO =====
    paginator = Paginator(posts_qs, 5)  # 5 posts por página
    page_number = request.GET.get("page")
    posts_page = paginator.get_page(page_number)

    if "all" in filters or not filters:
        posts = posts_page
        users = users_qs

    elif "posts" in filters:
        posts = posts_page

    elif "users" in filters:
        users = users_qs

    return render(
        request,
        "search/search_results.html",
        {
            "query": query,
            "posts": posts,
            "users": users,
        },
    )