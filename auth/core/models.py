from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.phone,)


class ProjectUsers(models.Model):
    userId = models.CharField(max_length=100)
    projectId = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return "%s - %s" % (self.userId, self.projectId,)