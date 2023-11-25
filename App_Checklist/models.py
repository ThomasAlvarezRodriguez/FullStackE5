from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Jeu(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.nom
    
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    jeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)


    def __str__(self):
        return self.nom
    
class Quete(models.Model):
    id = models.AutoField(primary_key=True)
    jeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

class ProfilUtilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jeux_favoris = models.ManyToManyField(Jeu)

    def __str__(self):
        return self.user.username
    
from django.conf import settings

class ProgressionItem(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    obtenu = models.BooleanField(default=False)

    class Meta:
        unique_together = ('utilisateur', 'item')

class ProgressionQuete(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quete = models.ForeignKey(Quete, on_delete=models.CASCADE)
    obtenu = models.BooleanField(default=False)

    class Meta:
        unique_together = ('utilisateur', 'quete')
