from .models import MyUser, Task, Subtask, Category
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
 
class SubtaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'checked']
        
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'color']
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    subtasks = SubtaskSerializer(many=True) 
    category = CategorySerializer()
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'assignedTo', 'status', 'priority', 'category', 'subtasks']
        
    def update(self, instance, validated_data):
        # Handhabung der Aktualisierung von Category
        category_data = validated_data.pop('category', None)
        if category_data:
            category_name = category_data.get('name')
            if category_name:
                # Finden der Kategorie anhand des Namens
                category_instance = Category.objects.get(name=category_name)
                instance.category = category_instance

        # Handhabung der Aktualisierung von Subtasks
        subtasks_data = validated_data.pop('subtasks', [])
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id', None)
            if subtask_id:
                Subtask.objects.filter(id=subtask_id, task=instance).update(**subtask_data)
            else:
                Subtask.objects.create(task=instance, **subtask_data)

        # Aktualisierung der restlichen Felder des Task
        return super(TaskSerializer, self).update(instance, validated_data)