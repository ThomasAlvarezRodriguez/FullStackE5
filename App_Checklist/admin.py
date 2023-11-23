from django.contrib import admin
from .models import Jeu, Item, Quete, ProfilUtilisateur

# Enregistrez vos modèles ici
admin.site.register(Jeu)
admin.site.register(Item)
admin.site.register(Quete)
admin.site.register(ProfilUtilisateur)
