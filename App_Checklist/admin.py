from django.contrib import admin
from .models import Jeu, Item, Quete, ProfilUtilisateur, Tag

# Enregistrez vos modèles ici
admin.site.register(Jeu)
admin.site.register(ProfilUtilisateur)
admin.site.register(Tag)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

@admin.register(Quete)
class QueteAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
