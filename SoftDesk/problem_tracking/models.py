from django.db import models
# from django.contrib.auth import get_user


PROJECT_TYPES = [('BE', 'Back-end'),
                 ('FE', 'Front-end'),
                 ('IOS', 'IOS'),
                 ('AND', 'Android')]
PRIORITES = [('F', 'FAIBLE'),
             ('M', 'MOYENNE'),
             ('E', 'ELEVEE')]
BALISES = [('BUG', 'BUG'),
           ('AMELIORATION', 'AMELIORATION'),
           ('TACHE', 'TACHE')]
STATUT = [('A_FAIRE', 'A faire'),
          ('EN_COURS', 'En cours'),
          ('TERMINE', 'Terminé')]

class Projet(models.Model):
    titre = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(choices=PROJECT_TYPES, max_length=30)


class Probleme(models.Model):
    titre = models.CharField(max_length=50)
    description = models.TextField()
    priorite = models.CharField(max_length=50, choices=PRIORITES)
    balise = models.CharField(max_length=50, choices=BALISES)
    statut = models.CharField(max_length=50, choices=STATUT)
    created_time = models.DateTimeField(auto_now_add=True)


class Commentaire(models.Model):
    description = models.TextField()
