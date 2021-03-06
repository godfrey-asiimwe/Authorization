"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MeView, Users, ProjectUser, ChangePasswordView
from .viewsets import ContactViewSet

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('users/', Users.as_view(), name='users'),
    path('create/', views.add_projects, name='add-projects'),
    path('projectusers/', ProjectUser.as_view(), name='projectusers'),
    path('prousers/<int:pk>', views.getUserByProjectId),
    path('contacts/',views.Contacts.as_view()),
    path('contact/<int:pk>', views.getContactByUser),
    path('update/<int:pk>', views.update_contacts),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),

]

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
urlpatterns += router.urls
