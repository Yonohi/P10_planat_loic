from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer, ContributorSerializer
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_user(self.request)
        return Project.objects.filter(auteur=user)


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Issue.objects.filter(projet=self.kwargs['project_pk'])
        else:
            return Issue.objects.all()

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'issue_pk' in self.kwargs:
            return Comment.objects.filter(probleme=self.kwargs['issue_pk'])
        else:
            return Comment.objects.all()


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()


class ContributorViewset(GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Contributor.objects.filter(project=self.kwargs['project_pk'])
        # remplacer par une erreur car on ne doit pas pouvoir voir ces données, pareil pour la plupart des autres viewset
        else:
            return Contributor.objects.all()


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

