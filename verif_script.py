from App_Checklist.models import Jeu
jeux = Jeu.objects.all()
for jeu in jeux:
    print(f'Nom: {jeu.nom}, Genre: {jeu.genre}, Description: {jeu.description}')
from App_Checklist.models import Item
items = Item.objects.all()
for item in items:
    print(f'Nom: {item.nom}, Jeu: {item.jeu.nom}, Description: {item.description}')
from App_Checklist.models import Quete
quetes = Quete.objects.all()
for quete in quetes:
    print(f'nom: {quete.nom}, Jeu: {quete.jeu.nom}, Description: {quete.description}')
from App_Checklist.models import ProfilUtilisateur
profils = ProfilUtilisateur.objects.all()
for profil in profils:
    jeux_favoris = ', '.join([jeu.nom for jeu in profil.jeux_favoris.all()])
    print(f'Utilisateur: {profil.user.username}, Jeux favoris: {jeux_favoris}')
print('Fin du script de vérification.')