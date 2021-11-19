from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Contributor, Project
from django.contrib.auth import get_user


"""
class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.auteur:
            if obj.auteur == request.user:
                return True
        else:
            return False

"""

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif obj.auteur == request.user:
            return True
        else:
            return False

# permission pour acceder aux issues d'un projet
class IsContributor(BasePermission):
    message = "Vous n'avez pas la permission d'effectuer cette action. " \
              "Vous ne faites pas partie des contributeurs du projet"
    def has_permission(self, request, view):
        if Contributor.objects.filter(project=view.kwargs['project_pk'],
                                        user=get_user(request)):
            return True
        else:
            return False
