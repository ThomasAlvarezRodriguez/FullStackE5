from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
    total_items = items.count()
    total_quetes = quetes.count()
    
    # Supposons que vous ayez une manière de savoir quels items et quêtes ont été obtenus
    # Par exemple, via un modèle Progression avec un booléen obtenu pour chaque item/quete
    items_obtenus = items.filter(progression__obtenu=True).count()
    quetes_obtenues = quetes.filter(progression__obtenu=True).count()

    # Calculez la progression
    progression_items = (items_obtenus / total_items) * 100 if total_items > 0 else 0
    progression_quetes = (quetes_obtenues / total_quetes) * 100 if total_quetes > 0 else 0

    context = {
        'jeu': jeu,
        'progression_items': progression_items,
        'progression_quetes': progression_quetes,
        # autres contextes...
    }
    return render(request, 'game_detail.html', context)


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    jeu = item.jeu  # Assurez-vous que l'item a une relation avec un jeu
    progression_url = reverse('update_progression_item', kwargs={'item_id': item.id})
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
from .models import Jeu, ProfilUtilisateur

@login_required
def toggle_favoris(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    profil_utilisateur, created = ProfilUtilisateur.objects.get_or_create(user=request.user)

    if jeu in profil_utilisateur.jeux_favoris.all():
        profil_utilisateur.jeux_favoris.remove(jeu)
    else:
        profil_utilisateur.jeux_favoris.add(jeu)

    return redirect('jeux_list')  # Redirigez l'utilisateur vers la liste des jeux

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Item, ProgressionItem, Quete, ProgressionQuete

@login_required
def update_progression_item(request):
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('item_'):
                item_id = key.split('_')[1]
                item = Item.objects.get(id=item_id)
                obtenu = request.POST[key] == 'on'
                ProgressionItem.objects.update_or_create(
                    utilisateur=request.user, item=item,
                    defaults={'obtenu': obtenu}
                )
        # Vous pouvez ajouter une gestion similaire pour les quêtes ici.
    return redirect('some_view_name')

@login_required
def update_progression_quete(request):
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('quete'):
                quete_id = key.split('_')[1]
                quete = Quete.objects.get(id=quete_id)
                obtenu = request.POST[key] == 'on'
                ProgressionQuete.objects.update_or_create(
                    utilisateur=request.user, quete=quete,
                    defaults={'obtenu': obtenu}
                )
        # Vous pouvez ajouter une gestion similaire pour les quêtes ici.
    return redirect('some_view_name')
