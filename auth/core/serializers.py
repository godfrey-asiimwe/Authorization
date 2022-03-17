from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models
from django.contrib.auth import get_user_model
from .models import Contact, ProjectUsers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUsers
        fields = ('id', 'userId', 'projectId')


class ContactSerializer(serializers.ModelSerializer):
    # Create new contact associated with current authenticated user
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        contact = super().create(validated_data)
        return contact

    class Meta:
        model = Contact
        exclude = ('user',)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
