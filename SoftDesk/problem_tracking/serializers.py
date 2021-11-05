from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Project, Issue, Comment, Contributor

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'titre', 'description', 'type', 'auteur']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'titre', 'description', 'assigne', 'priorite', 'balise', 'statut', 'created_time', 'projet']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'auteur', 'probleme']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'project', 'permission', 'role']