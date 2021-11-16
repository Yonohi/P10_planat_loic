from rest_framework import serializers
from rest_framework import request
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # Autre manière d'afficher tous les champs
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'titre', 'description', 'assigne', 'priorite', 'balise', 'statut', 'created_time', 'projet']
        read_only_fields = ['projet']
    # Attention à ne pas le mettre dans la classe meta
    def validate(self, validated_data):
        test = self.context
        if self.context['request'].method == 'POST':
            validated_data['description'] = test
            validated_data['projet'] = Project.objects.filter(id=1)[0]
        return validated_data
    def create(self, validated_data):
        return Issue.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'auteur', 'probleme']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    # cette méthode est nécessaire ou en tout cas c'est la façon que j'ai
    # trouvé pour avoir le hashage du password, sinon le user est crée mais
    # le mot de passe ne convient pas
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'project', 'permission', 'role']