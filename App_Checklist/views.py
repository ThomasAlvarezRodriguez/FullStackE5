from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm

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
    if request.user.is_authenticated:
        profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)
        progress_per_game = {}
        for jeu in jeux:
            items = Item.objects.filter(jeu=jeu)
            quetes = Quete.objects.filter(jeu=jeu)
            total_points = sum(item.points for item in items) + sum(quete.points for quete in quetes)
            obtained_points = sum(item.points for item in profil_utilisateur.items_obtenus.filter(jeu=jeu)) + sum(quete.points for quete in profil_utilisateur.quetes_obtenues.filter(jeu=jeu))
            progress = (obtained_points / total_points * 100) if total_points else 0
            progress_per_game[jeu.id] = progress
        return render(request, 'jeux_list.html', {
            'profil_utilisateur': profil_utilisateur,
            'jeux': jeux,
            'progress_per_game': progress_per_game,  })
        
    return render(request, 'jeux_list.html', {'jeux': jeux})


from django.shortcuts import render

def game(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    items = Item.objects.filter(jeu=jeu)
    quetes = Quete.objects.filter(jeu=jeu)

    if request.user.is_authenticated:
        profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)
        
        # Compute the obtained status and points for items
        items_with_status = [(item, item in profil_utilisateur.items_obtenus.all(), item.points)
                             for item in items]
        # Compute the obtained status and points for quests
        quetes_with_status = [(quete, quete in profil_utilisateur.quetes_obtenues.all(), quete.points)
                              for quete in quetes]

        # Calculate the total and user-obtained points for items and quests
        total_items_points = sum(item.points for item in items)
        total_quetes_points = sum(quete.points for quete in quetes)
        user_items_points = sum(status[2] for status in items_with_status if status[1])
        user_quetes_points = sum(status[2] for status in quetes_with_status if status[1])

        # Calculate progress as a percentage
        items_progress = (user_items_points / total_items_points * 100) if total_items_points else 0
        quetes_progress = (user_quetes_points / total_quetes_points * 100) if total_quetes_points else 0
    else:
        # For unauthenticated users, show no progress and set all statuses to False
        items_with_status = [(item, False, item.points) for item in items]
        quetes_with_status = [(quete, False, quete.points) for quete in quetes]
        total_items_points = sum(item.points for item in items)
        total_quetes_points = sum(quete.points for quete in quetes)
        user_items_points = user_quetes_points = items_progress = quetes_progress = 0

    context = {
        'jeu': jeu,
        'items_with_status': items_with_status,
        'quetes_with_status': quetes_with_status,
        'items_progress': items_progress,
        'quetes_progress': quetes_progress,
        'user_items_points': user_items_points,
        'total_items_points': total_items_points,
        'user_quetes_points': user_quetes_points,
        'total_quetes_points': total_quetes_points,
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
    profil_utilisateur, created = ProfilUtilisateur.objects.get_or_create(user=request.user)
    jeux_favoris = profil_utilisateur.jeux_favoris.all()

    progress_per_game = {}
    for jeu in jeux_favoris:
        items = Item.objects.filter(jeu=jeu)
        quetes = Quete.objects.filter(jeu=jeu)
        total_points = sum(item.points for item in items) + sum(quete.points for quete in quetes)
        obtained_points = sum(item.points for item in profil_utilisateur.items_obtenus.filter(jeu=jeu)) + sum(quete.points for quete in profil_utilisateur.quetes_obtenues.filter(jeu=jeu))
        progress = (obtained_points / total_points * 100) if total_points else 0
        progress_per_game[jeu.id] = progress

    return render(request, 'profile.html', {
        'profil_utilisateur': profil_utilisateur,
        'jeux_favoris': jeux_favoris,
        'progress_per_game': progress_per_game,
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
    item_points = getattr(item, 'points', 1)  # Get points or default to 0

    if item in profil_utilisateur.items_obtenus.all():
        profil_utilisateur.items_obtenus.remove(item)
        profil_utilisateur.points -= item_points
    else:
        profil_utilisateur.items_obtenus.add(item)
        profil_utilisateur.points += item_points
    profil_utilisateur.save()

    # Redirect back to the same page to show the updated status
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def toggle_obtenu_quete(request, quete_id):
    quete = get_object_or_404(Quete, pk=quete_id)
    profil_utilisateur = ProfilUtilisateur.objects.get(user=request.user)
    quete_points = getattr(quete, 'points', 1)  # Get points or default to 0

    if quete in profil_utilisateur.quetes_obtenues.all():
        profil_utilisateur.quetes_obtenues.remove(quete)
        profil_utilisateur.points -= quete_points
    else:
        profil_utilisateur.quetes_obtenues.add(quete)
        profil_utilisateur.points += quete_points

    profil_utilisateur.save()
    # Redirect back to the same page to show the updated status
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


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
        return HttpResponseRedirect(reverse('game', args=[jeu.id]))
    else:
        # If not a POST request, redirect to the game detail page without making changes
        return HttpResponseRedirect(reverse('game', args=[jeu_id]))

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import NewUserForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")  # Redirect to a home page or login page
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", {"register_form": form})

