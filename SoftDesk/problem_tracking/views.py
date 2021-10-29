from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Projet, Probleme, Commentaire
from .serializers import ProjetSerializer, ProblemeSerializer, CommentaireSerializer

class ProjetViewset(ModelViewSet):
    serializer_class = ProjetSerializer

    def get_queryset(self):
        return Projet.objects.all()


class ProblemeViewset(ModelViewSet):
    serializer_class = ProblemeSerializer

    def get_queryset(self):
        return Probleme.objects.all()


class CommentaireViewset(ModelViewSet):
    serializer_class = CommentaireSerializer

    def get_queryset(self):
        return Commentaire.objects.all()