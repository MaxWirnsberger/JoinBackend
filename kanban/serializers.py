from .models import MyUser, Task, Subtask, Category
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
 
class SubtaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subtask
        fields = ['title', 'checked']
        
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'color']
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    subtask = SubtaskSerializer(many=True) 
    category = CategorySerializer()
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_users', 'status', 'priority', 'category', 'subtask']