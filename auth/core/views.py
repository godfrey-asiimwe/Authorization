from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers

from .models import ProjectUsers
from .serializers import UserSerializer, ProjectUserSerializer


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
