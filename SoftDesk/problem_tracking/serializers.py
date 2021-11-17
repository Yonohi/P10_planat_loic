from rest_framework import serializers
from rest_framework import request
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'titre', 'description', 'type', 'auteur']
        read_only_fields = ['auteur']
    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['auteur'] = get_user(self.context['request'])
        return validated_data
    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'titre', 'description', 'assigne', 'priorite', 'balise', 'statut', 'projet', 'created_time']
        read_only_fields = ['projet', 'assigne']
    # Attention à ne pas le mettre dans la classe meta
    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            # On met la valeur de projet à celle du projet de l'endpoint
            validated_data['projet'] = Project.objects.filter(id=self.context['project_pk'])[0]
            # Meme chose pour l'assigne
            validated_data['assigne'] = get_user(self.context['request'])
        return validated_data
    def create(self, validated_data):
        return Issue.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'auteur', 'probleme', 'created_time']
        read_only_fields = ['auteur', 'probleme']
    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['probleme'] = Issue.objects.filter(id=self.context['issue_pk'])[0]
            validated_data['auteur'] = get_user(self.context['request'])
        return validated_data
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


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
        read_only_fields = ['project']
    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['project'] = Project.objects.filter(id=self.context['project_pk'])[0]
        return validated_data
    def create(self, validated_data):
        return Contributor.objects.create(**validated_data)