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
        fields = ('id', 'userId', 'projectId','role')


class ContactSerializer(serializers.ModelSerializer):
    # Create new contact associated with current authenticated user
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        contact = super().create(validated_data)
        return contact

    class Meta:
        model = Contact
        fields = ('id','user', 'name','email','phone','notes')


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
