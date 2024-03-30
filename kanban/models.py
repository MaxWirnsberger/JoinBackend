from django.db import models
from django.conf import settings
import datetime
from authemail.models import EmailUserManager, EmailAbstractUser

class MyUser(EmailAbstractUser):
    objects = EmailUserManager()
    
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=25)
    color = models.CharField(max_length=100)
    
    def __str__(self):
        return f'({self.id})  {self.name}'
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    due_date = models.DateField(default=datetime.date.today)
    assignedTo = models.ManyToManyField(Contact, blank=True)
    status = models.CharField(max_length=25, default="todo")
    priority = models.CharField(max_length=25, default="Low")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, default=None)
    
    def __str__(self):
        return f'({self.id})  {self.title}'
    

class Subtask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    checked = models.BooleanField(default=False) 
    
    def __str__(self):
        return f'{self.title}'