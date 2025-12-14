from django.contrib.auth import logout
from django.http import HttpResponse

def logout_view(request):
    logout(request)
    return HttpResponse("<script>alert('Logout successful'); window.location='/login';</script>")