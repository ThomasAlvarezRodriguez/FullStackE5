from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def profile_view(request):
    return render(request, 'profile.html')

def game_view(request):
    return render(request, 'game.html')

from .models import Jeu

def jeux_list(request):
    jeux = Jeu.objects.all()  # Récupère tous les jeux
    return render(request, 'jeux_list.html', {'jeux': jeux})
