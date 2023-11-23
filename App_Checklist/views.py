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

from .models import Item, Tag

def items_par_tags(request, tags):
    tag_list = tags.split('+')  # 'France+Terrestre' devient ['France', 'Terrestre']
    items = Item.objects.all()
    
    for tag_name in tag_list:
        items = items.filter(tags__nom=tag_name)
    
    context = {'items': items}
    return render(request, 'path/to/your_template.html', context)

from .models import Item, Tag

def liste_des_items(request):
    tags_disponibles = Tag.objects.all()
    items = Item.objects.all()

    # Si des tags sont sélectionnés, filtrez les items en conséquence.
    selected_tags = request.GET.getlist('tag')
    if selected_tags:
        items = items.filter(tags__nom__in=selected_tags).distinct()

    context = {
        'tags_disponibles': tags_disponibles,
        'items': items,
    }
    return render(request, 'chemin/vers/liste_des_items.html', context)

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Jeu, Tag

def detail_du_jeu(request, jeu_id):
    jeu = get_object_or_404(Jeu, pk=jeu_id)
    tags_disponibles = Tag.objects.filter(items__jeu=jeu).distinct()
    items = jeu.item_set.all()

    selected_tags = request.GET.getlist('tag')
    if selected_tags:
        items = items.filter(tags__nom__in=selected_tags).distinct()

    context = {
        'jeu': jeu,
        'tags_disponibles': tags_disponibles,
        'items': items,
    }
    return render(request, 'jeux/detail_du_jeu.html', context)
