"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework_nested import routers
from problem_tracking.views import (ProjectViewset, IssueViewset,
                                    CommentViewset, ContributorViewset,
                                    SignupView, my_login_view)
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

projects_router = routers.NestedSimpleRouter(router,
                                             r'projects',
                                             lookup='project')
projects_router.register(r'issues', IssueViewset, basename='issues')
projects_router.register(r'users', ContributorViewset, basename='contributors')

problemes_router = routers.NestedSimpleRouter(projects_router,
                                              r'issues',
                                              lookup='issue')
problemes_router.register(r'comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', my_login_view, name='log'),
    path('api/', include(router.urls)),
    path(r'api/', include(projects_router.urls)),
    path(r'api/', include(problemes_router.urls)),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
