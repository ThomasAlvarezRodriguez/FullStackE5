from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

def home_view(request):
    return render(request, 'home.html')

def profile_view(request):
    return render(request, 'profile.html')

def game_view(request):
    return render(request, 'game.html')

from .models import Jeu, Item

def jeux_list(request):
    jeux = Jeu.objects.all()  # Récupère tous les jeux
    return render(request, 'jeux_list.html', {'jeux': jeux})


def game_detail(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    items = Item.objects.filter(jeu=jeu)
    return render(request, 'game.html', {'jeu': jeu, 'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    jeu = item.jeu  # Assurez-vous que l'item a une relation avec un jeu
    return render(request, 'item_detail.html', {'item': item, 'jeu': jeu})

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # Obtenez le profil de l'utilisateur et ses jeux favoris
    profil_utilisateur = request.user.profilutilisateur
    jeux_favoris = profil_utilisateur.jeux_favoris.all()

    # Vous pouvez également inclure la progression de l'utilisateur dans les jeux ici
    # ...

    return render(request, 'profile.html', {
        'profil_utilisateur': profil_utilisateur,
        'jeux_favoris': jeux_favoris,
        # 'progression_jeux': progression_jeux, # Si vous avez les données de progression
    })