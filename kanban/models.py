from django.db import models
from django.conf import settings
from authemail.models import EmailUserManager, EmailAbstractUser

class MyUser(EmailAbstractUser):
    initials = models.CharField(max_length=5, null=True)
    color = models.CharField(max_length=10, null=True)
    objects = EmailUserManager()