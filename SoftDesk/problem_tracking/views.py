from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Project, Issue, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, UserSerializer, ContributorSerializer
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .permissions import IsAuthorOrReadOnly, IsContributor, IsLogged, ProjectAuthorOrContributorHimself


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsLogged]

    def get_queryset(self):
        return Project.objects.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    # IsLogged doit apparaitre avant IsContributor car l'utilisateur doit être
    # connecté pour vérifier s'il s'agit d'un contributeur
    permission_classes = [IsAuthenticated, IsLogged, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):

        if 'project_pk' in self.kwargs:
            return Issue.objects.filter(projet=self.kwargs['project_pk'])
        else:
            pass

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
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsLogged, IsContributor]

    def get_queryset(self):
        if 'issue_pk' in self.kwargs:
            return Comment.objects.filter(probleme=self.kwargs['issue_pk'])
        else:
            pass

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


class ContributorViewset(GenericViewSet, CreateModelMixin, ListModelMixin, DestroyModelMixin):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsLogged, IsContributor, ProjectAuthorOrContributorHimself]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Contributor.objects.filter(project=self.kwargs['project_pk'])
        # remplacer par une erreur car on ne doit pas pouvoir voir ces données, pareil pour la plupart des autres viewset
        else:
            pass

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
