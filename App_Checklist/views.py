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


from django.shortcuts import render

def game_detail(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    items = Item.objects.filter(jeu=jeu)
    profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)

    # Include whether each item is obtained in the template context
    items_with_status = [(item, item in profil_utilisateur.items_obtenus.all()) for item in items]

    return render(request, 'game_detail.html', {
        'jeu': jeu,
        'items_with_status': items_with_status,
        # Include other necessary context
    })


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
from .models import Jeu, ProfilUtilisateur, Item, Quete

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
    profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)

    if item in profil_utilisateur.items_obtenus.all():
        profil_utilisateur.items_obtenus.remove(item)
    else:
        profil_utilisateur.items_obtenus.add(item)
    profil_utilisateur.save()

    # Make sure to redirect to a view that shows the item, such as the item detail or game detail view
    return redirect('game_detail', jeu_id=item.jeu.id)

@login_required
def toggle_obtenu_quete(request, quete_id):
    quete = get_object_or_404(Quete, pk=quete_id)
    profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)

    # Toggle the quest obtained status
    if quete in profil_utilisateur.quetes_obtenues.all():
        profil_utilisateur.quetes_obtenues.remove(quete)
    else:
        profil_utilisateur.quetes_obtenues.add(quete)

    profil_utilisateur.save()

    # Redirect to the 'game_detail' view with the correct 'jeu_id' argument
    return redirect('game_detail', jeu_id=quete.jeu.id)

from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def update_progression(request, jeu_id):
    if request.method == 'POST':
        profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)
        jeu = get_object_or_404(Jeu, pk=jeu_id)
        
        # Update items
        items = Item.objects.filter(jeu=jeu)
        for item in items:
            item_checkbox = request.POST.get(f'item_{item.id}', False)
            if item_checkbox and not item in profil_utilisateur.items_obtenus.all():
                profil_utilisateur.items_obtenus.add(item)
            elif not item_checkbox and item in profil_utilisateur.items_obtenus.all():
                profil_utilisateur.items_obtenus.remove(item)
        
        # Update quests
        quetes = Quete.objects.filter(jeu=jeu)
        for quete in quetes:
            quete_checkbox = request.POST.get(f'quete_{quete.id}', False)
            if quete_checkbox and not quete in profil_utilisateur.quetes_obtenues.all():
                profil_utilisateur.quetes_obtenues.add(quete)
            elif not quete_checkbox and quete in profil_utilisateur.quetes_obtenues.all():
                profil_utilisateur.quetes_obtenues.remove(quete)
        
        # Save the profile after making changes
        profil_utilisateur.save()
        
        # Redirect to the game detail page
        return HttpResponseRedirect(reverse('game_detail', args=[jeu.id]))
    else:
        # If not a POST request, redirect to the game detail page without making changes
        return HttpResponseRedirect(reverse('game_detail', args=[jeu_id]))

