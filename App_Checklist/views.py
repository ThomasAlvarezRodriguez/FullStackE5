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


from django.shortcuts import redirect
from django.conf import settings

def keycloak_login(request):
    redirect_uri = request.build_absolute_uri('/callback/')  # Adjust the callback URL
    return redirect(
        f'{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth?client_id={settings.KEYCLOAK_CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}'
    )



import requests
from django.conf import settings
from django.http import JsonResponse

def keycloak_callback(request):
    code = request.GET.get('code')
    redirect_uri = 'https://devliste5-880bb90a4eca.herokuapp.com/callback/'  # Adjust the callback URL

    # Exchange code for token
    response = requests.post(
        f'{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token',
        data={
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'client_secret': settings.KEYCLOAK_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
    )
    response_data = response.json()
    access_token = response_data.get('access_token')

    # Optionally: Fetch user info
    user_info_response = requests.get(
        f'{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    user_info = user_info_response.json()

    # Process user info as needed
    # ...

    return JsonResponse(user_info)
