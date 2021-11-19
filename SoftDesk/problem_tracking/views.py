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
from rest_framework import status
from .permissions import IsAuthorOrReadOnly, IsContributor
from itertools import chain

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.all()

    """
    Quelques essais à voir avec mon mentor:
        def get_queryset(self):
        user = get_user(self.request)
        contributor = Contributor.objects.filter(user=user)[0]
        projects = Project.objects.filter(auteur=user)
        projects_contrib = Project.objects.filter(contributors=contributor)
        all_proj = projects | projects_contrib
        return all_proj
    
        def get_queryset(self):
        user = get_user(self.request)
        all_projects = []
        contributors = Contributor.objects.filter(user=user)
        projects = Project.objects.filter(auteur=user)
        for project in projects:
            if project not in all_projects:
                all_projects.append(project)
        for contributor in contributors:
            if contributor.project not in all_projects:
                all_projects.append(contributor.project)
        return sorted(all_projects, key=lambda x:x.id)
    """



class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):

        if 'project_pk' in self.kwargs:
            return Issue.objects.filter(projet=self.kwargs['project_pk'])
        else:
            # mettre plus tard que le projet n'existe pas
            return Issue.objects.all()

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'project_pk': self.kwargs['project_pk'],
            'request': request,
        }
        serializer = IssueSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsContributor]

    def get_queryset(self):
        if 'issue_pk' in self.kwargs:
            return Comment.objects.filter(probleme=self.kwargs['issue_pk'])
        else:
            return Comment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'issue_pk': self.kwargs['issue_pk'],
            'request': request,
        }
        serializer = CommentSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

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
    def create(self, request, *args, **kwargs):
        serializer_context = {
            'project_pk': self.kwargs['project_pk'],
            'request': request,
        }
        serializer = ContributorSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

