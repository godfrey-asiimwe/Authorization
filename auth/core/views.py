from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers

from .models import ProjectUsers, Contact
from .serializers import UserSerializer, ProjectUserSerializer, ChangePasswordSerializer, ContactSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class Users(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_projects(request):
    project = ProjectUserSerializer(data=request.data)
    # validating for already existing data
    if ProjectUsers.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if project.is_valid():
        project.save()
        return Response(project.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProjectUser(APIView):
    def get(self, request):
        users = ProjectUsers.objects.all()
        serializer = ProjectUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Contacts(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getUserByProjectId(request, pk):
    users = ProjectUsers.objects.all().filter(projectId=pk)

    userinfo = []
    for user in users:
        userinfo += User.objects.all().filter(id=user.userId)

    serializer = UserSerializer(userinfo, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getContactByUser(request, pk):
    contacts = Contact.objects.all().filter(user=pk)

    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


@api_view(['POST'])
def update_contacts(request, pk):
    contact = Contact.objects.get(pk=pk)
    data = ContactSerializer(instance=contact, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
