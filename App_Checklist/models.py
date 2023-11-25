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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jeux_favoris = models.ManyToManyField(Jeu)
    items_obtenus = models.ManyToManyField(Item, blank=True)
    quetes_obtenues = models.ManyToManyField(Quete, blank=True)

    def __str__(self):
        return self.user.username
