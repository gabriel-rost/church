from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator

@user_passes_test(lambda u: u.is_superuser)
def manage_users(request):
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        target_user = get_object_or_404(User, id=user_id)

        if action == 'approve':
            target_user.is_approved = True
            target_user.accepted_at = timezone.now()
            messages.success(request, f"Irmão {target_user.username} aprovado!")
        
        elif action == 'make_admin':
            target_user.is_staff = True
            messages.info(request, f"{target_user.username} agora é Staff.")
        
        elif action == 'remove_admin':
            target_user.is_staff = False
            messages.warning(request, f"Privilégios removidos de {target_user.username}.")

        target_user.save()
        return redirect('manage_users')

    users_list = User.objects.all().order_by('-date_joined')
    
    paginator = Paginator(users_list, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
    }
    
    return render(request, 'admin_custom/manage_users.html', context)