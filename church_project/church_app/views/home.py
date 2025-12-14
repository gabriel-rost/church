from django.shortcuts import render
from ..models import Channel

def home(request):
    channels = Channel.objects.all()
    return render(request, "home.html", {"channels": channels})