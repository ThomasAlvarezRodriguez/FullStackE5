from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'home.html')

@login_required
def profile_view(request):
    profil_utilisateur, created = ProfilUtilisateur.objects.get_or_create(user=request.user)
    jeux_favoris = profil_utilisateur.jeux_favoris.all()

    return render(request, 'profile.html', {
        'profil_utilisateur': profil_utilisateur,
        'jeux_favoris': jeux_favoris,
    })

def game_view(request):
    return render(request, 'game.html')

from .models import Jeu, Item, Quete

def jeux_list(request):
    jeux = Jeu.objects.all()  # Récupère tous les jeux
    return render(request, 'jeux_list.html', {'jeux': jeux})


def game_detail(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    items = Item.objects.filter(jeu=jeu)
    quetes = Quete.objects.filter(jeu=jeu)
    # Ajoutez les fonctions au contexte pour qu'elles soient utilisables dans le template
    context = {
        'jeu': jeu,
        'items': items,
        'quetes': quetes,
        'user_has_item': user_has_item,
        'user_has_quete': user_has_quete,
        'user': request.user,
    }
    return render(request, 'game.html', context)

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    jeu = item.jeu  # Assurez-vous que l'item a une relation avec un jeu
    return render(request, 'item_detail.html', {'item': item, 'jeu': jeu})

def quete_detail(request, quete_id):
    quete = get_object_or_404(Quete, pk=quete_id)
    jeu = quete.jeu  
    return render(request, 'quete_detail.html', {'quete': quete, 'jeu': jeu})

@login_required
def profile_view(request):
    user = request.user
    profil_utilisateur, created = ProfilUtilisateur.objects.get_or_create(user=user)
    jeux_favoris = profil_utilisateur.jeux_favoris.all()

    return render(request, 'profile.html', {
        'profil_utilisateur': profil_utilisateur,
        'jeux_favoris': jeux_favoris,
    })

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfilUtilisateur

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfilUtilisateur.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profilutilisateur.save()

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Jeu, ProfilUtilisateur, Item, Quete, ProgressionItem, ProgressionQuete

@login_required
def toggle_favoris(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    profil_utilisateur, created = ProfilUtilisateur.objects.get_or_create(user=request.user)

    if jeu in profil_utilisateur.jeux_favoris.all():
        profil_utilisateur.jeux_favoris.remove(jeu)
    else:
        profil_utilisateur.jeux_favoris.add(jeu)

    return redirect('jeux_list')  # Redirigez l'utilisateur vers la liste des jeux

@login_required
def toggle_obtenu_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    progression, created = ProgressionItem.objects.get_or_create(utilisateur=request.user, item=item)
    progression.obtenu = not progression.obtenu
    progression.save()
    return redirect('chemin_retour')

@login_required
def toggle_obtenu_quete(request, quete_id):
    quete = get_object_or_404(Quete, pk=quete_id)
    progression, created = ProgressionQuete.objects.get_or_create(utilisateur=request.user, quete=quete)
    progression.accomplie = not progression.accomplie
    progression.save()
    return redirect('chemin_retour')