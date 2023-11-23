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
    
class Tag(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom
        
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    jeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='items')


    def __str__(self):
        return self.nom
    
class Quete(models.Model):
    id = models.AutoField(primary_key=True)
    jeu = models.ForeignKey(Jeu, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='quetes')


    def __str__(self):
        return self.titre

class ProfilUtilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jeux_favoris = models.ManyToManyField(Jeu)

    def __str__(self):
        return self.user.username