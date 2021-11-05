from django.db import models
from django.conf import settings
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
STATUTS = [('A_FAIRE', 'A faire'),
           ('EN_COURS', 'En cours'),
           ('TERMINE', 'Terminé')]
PERMISSIONS = []
ROLES = [('AUTHOR', 'Auteur'),
         ('MANAGER', 'Responsable'),
         ('CREATOR', 'Créateur')]

class Project(models.Model):
    titre = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(choices=PROJECT_TYPES, max_length=30)
    auteur = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='projects',
                               default=0)

    def __str__(self):
        return self.titre


class Issue(models.Model):
    titre = models.CharField(max_length=50)
    description = models.TextField()
    assigne = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='issues',
                                default=0)
    priorite = models.CharField(max_length=50, choices=PRIORITES)
    balise = models.CharField(max_length=50, choices=BALISES)
    statut = models.CharField(max_length=50, choices=STATUTS)
    created_time = models.DateTimeField(auto_now_add=True)
    projet = models.ForeignKey('Project',
                               on_delete=models.CASCADE,
                               related_name='issues',
                               default=0)

    def __str__(self):
        return self.titre


class Comment(models.Model):
    description = models.TextField()
    auteur = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               default=0)
    probleme = models.ForeignKey('Issue',
                                 on_delete=models.CASCADE,
                                 related_name='comments',
                                 default=0)


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='contributors',
                               default=0)
    project = models.ForeignKey('Project',
                               on_delete=models.CASCADE,
                               related_name='contributors',
                               default=0)
    permission = models.CharField(max_length=50, choices=PERMISSIONS)
    role = models.CharField(max_length=50, choices=ROLES)