from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Issue, Comment, Contributor
from django.contrib.auth import get_user
import django.contrib.auth.password_validation as validators


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_id']
        read_only_fields = ['author_id']

    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['author'] = get_user(self.context['request'])
        return validated_data

    # We created our contributor (author) at the same time as the project
    def create(self, validated_data):
        project_created = Project.objects.create(**validated_data)
        Contributor.objects.create(user=validated_data['author'],
                                   project=project_created,
                                   permission='all',
                                   role='AUTHOR')
        return project_created


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id',
                  'title',
                  'description',
                  'assignee_user',
                  'assignee_user_id',
                  'author_id',
                  'priority',
                  'tag',
                  'status',
                  'project_id',
                  'created_time']
        read_only_fields = ['project_id', 'author_id', 'assignee_user_id']
        extra_kwargs = {
            'assignee_user': {'write_only': True}
        }

    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            # 'projet' automatically filled
            validated_data['project'] = Project.objects.filter(
                id=self.context['project_pk'])[0]
            # 'auteur' automatically filled
            validated_data['author'] = get_user(self.context['request'])
        return validated_data

    def create(self, validated_data):
        return Issue.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_id', 'issue_id', 'created_time']
        read_only_fields = ['author_id', 'issue_id']

    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['issue'] = Issue.objects.filter(
                id=self.context['issue_pk'])[0]
            validated_data['author'] = get_user(self.context['request'])
        return validated_data

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'password']

    # create_user to have the hash
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # password not check with create_user, need the following code
    @staticmethod
    def validate_password(data):
        validators.validate_password(password=data, user=User)
        return data


class ContributorSerializer(serializers.ModelSerializer):
    # utilisateur = serializers.CharField(source='user')
    # projet =serializers.CharField(source='project')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'user_id', 'project_id', 'permission', 'role']
        read_only_fields = ['project', 'user_id']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, validated_data):
        if self.context['request'].method == 'POST':
            validated_data['project'] = Project.objects.filter(
                id=self.context['project_pk'])[0]
        return validated_data

    def create(self, validated_data):
        return Contributor.objects.create(**validated_data)
