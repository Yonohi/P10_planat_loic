from rest_framework.serializers import ModelSerializer
from .models import Projet, Probleme, Commentaire

class ProjetSerializer(ModelSerializer):
    class Meta:
        model = Projet
        fields = ['titre', 'description', 'type']


class ProblemeSerializer(ModelSerializer):
    class Meta:
        model = Probleme
        fields = ['titre', 'description', 'priorite', 'balise', 'statut', 'created_time']


class CommentaireSerializer(ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['description']