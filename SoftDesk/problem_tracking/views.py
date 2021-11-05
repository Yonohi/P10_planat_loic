from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer, ContributorSerializer
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Issue.objects.filter(projet=self.kwargs['project_pk'])
        else:
            return Issue.objects.all()

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        if 'probleme_pk' in self.kwargs:
            return Comment.objects.filter(probleme=self.kwargs['probleme_pk'])
        else:
            return Comment.objects.all()


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class ContributorViewset(GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Contributor.objects.filter(project=self.kwargs['project_pk'])
        else:
            return Contributor.objects.all()

