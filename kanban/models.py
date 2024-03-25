from django.db import models
from django.conf import settings
import datetime
from authemail.models import EmailUserManager, EmailAbstractUser

class MyUser(EmailAbstractUser):
    objects = EmailUserManager()
    
class Contacts(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=25)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField(default=datetime.date.today)
    assigned_users = models.ManyToManyField(Contacts, default=None)
    status = models.CharField(max_length=25, default="todo")
    priority = models.CharField(max_length=25, default="low")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default=None)
    
class Subtasks(models.Model):
    title = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)