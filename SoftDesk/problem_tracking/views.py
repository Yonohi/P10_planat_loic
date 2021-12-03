from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Project, Issue, Comment, Contributor
from .serializers import (ProjectSerializer,
                          IssueSerializer,
                          CommentSerializer,
                          UserSerializer,
                          ContributorSerializer)
from rest_framework.mixins import (DestroyModelMixin,
                                   CreateModelMixin,
                                   ListModelMixin)
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import (IsAuthorOrReadOnly,
                          IsContributor,
                          IsLogged,
                          ProjectAuthorOrContributorHimself)
from rest_framework.decorators import api_view, permission_classes


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly, IsLogged]

    def get_queryset(self):
        return Project.objects.all()


class IssueViewset(ModelViewSet):
    serializer_class = IssueSerializer
    # IsLogged should be before IsContributor because the user should be
    # connected to verify if it's a contributor
    permission_classes = [IsAuthenticated,
                          IsLogged,
                          IsContributor,
                          IsAuthorOrReadOnly]

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
        serializer = IssueSerializer(data=request.data,
                                     context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,
                          IsAuthorOrReadOnly,
                          IsLogged,
                          IsContributor]

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
        serializer = CommentSerializer(data=request.data,
                                       context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class ContributorViewset(GenericViewSet,
                         CreateModelMixin,
                         ListModelMixin,
                         DestroyModelMixin):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated,
                          IsLogged,
                          IsContributor,
                          ProjectAuthorOrContributorHimself]

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Contributor.objects.filter(
                project=self.kwargs['project_pk'])
        else:
            pass

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'project_pk': self.kwargs['project_pk'],
            'request': request,
        }
        serializer = ContributorSerializer(data=request.data,
                                           context=serializer_context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def my_login_view(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                user_details = dict()
                user_details['username'] = username
                refresh = RefreshToken.for_user(user)
                user_details['token_access'] = str(refresh.access_token)
                user_details['token_refresh'] = str(refresh)
                login(request, user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as error:
                raise error
        else:
            message = {
                'error': 'Le username ou le password ne convient pas.'}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        message = {'error': 'Veuillez rentrer un username et un password.'}
        return Response(message)
