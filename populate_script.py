import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BackList.settings')
django.setup()

from django.contrib.auth.models import User
from App_Checklist.models import Jeu, Item, Quete, ProfilUtilisateur

def create_jeu(nom, genre, description, image=None):
    jeu = Jeu(nom=nom, genre=genre, description=description, image=image)
    jeu.save()
    return jeu

def create_item(jeu, nom, description, image=None):
    item = Item(jeu=jeu, nom=nom, description=description, image=image)
    item.save()

def create_quete(jeu, nom, description):
    quete = Quete(jeu=jeu, nom=nom, description=description)
    quete.save()

def create_profil_utilisateur(user, jeux_favoris):
    profil = ProfilUtilisateur(user=user)
    profil.save()
    profil.jeux_favoris.set(jeux_favoris)
    profil.save()

def populate():
    # Créer des jeux
    jeu1 = create_jeu('Jeu 1', 'Genre 1', 'Description Jeu 1')
    jeu2 = create_jeu('Jeu 2', 'Genre 2', 'Description Jeu 2')

    # Créer des items
    create_item(jeu1, 'Item 1 de Jeu 1', 'Description Item 1')
    create_item(jeu2, 'Item 1 de Jeu 2', 'Description Item 1')

    # Créer des quêtes
    create_quete(jeu1, 'Quête 1 de Jeu 1', 'Description Quête 1')
    create_quete(jeu2, 'Quête 1 de Jeu 2', 'Description Quête 1')

    # Créer des utilisateurs et des profils
    user1 = User.objects.create_user('user1', 'user1@example.com', 'user1password')
    user2 = User.objects.create_user('user2', 'user2@example.com', 'user2password')

    create_profil_utilisateur(user1, [jeu1, jeu2])
    create_profil_utilisateur(user2, [jeu1, jeu2])

    print("Base de données peuplée avec succès !")

if __name__ == '__main__':
    populate()
