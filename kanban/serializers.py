from .models import MyUser, Task, Subtask, Category, Contact
from rest_framework import serializers


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
 
class SubtaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'checked', 'task']
        
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'color']
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    subtasks = SubtaskSerializer(many=True) 
    category = CategorySerializer()
    assignedTo = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Contact.objects.all(),
        required=False 
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'assignedTo', 'status', 'priority', 'category', 'subtasks']
    
    def update(self, instance, validated_data):
        assignedTo_data = validated_data.pop('assignedTo', None)
        if assignedTo_data is not None:
            instance.assignedTo.set(assignedTo_data)    
    
        category_data = validated_data.pop('category', None)
        if category_data:
            category_name = category_data.get('name')
            if category_name:
                category_instance = Category.objects.get(name=category_name)
                instance.category = category_instance

        subtasks_data = validated_data.pop('subtasks', [])
        for subtask_data in subtasks_data:
            subtask_id = subtask_data.pop('id', None)  
            subtask_data.pop('task', None)  
            if subtask_id:
                Subtask.objects.filter(id=subtask_id, task=instance).update(**subtask_data)
            else:
                Subtask.objects.create(task=instance, **subtask_data)
                
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
    def create(self, validated_data):
        # Extrahieren der assignedTo-Daten und Entfernen aus dem validated_data
        assignedTo_data = validated_data.pop('assignedTo', [])

        # Extrahieren und Entfernen der Subtask-Daten
        subtasks_data = validated_data.pop('subtasks', [])
        category_data = validated_data.pop('category', None)

        # Erstellen der Kategorie, falls erforderlich
        if category_data:
            category_name = category_data.get('name')
            category, created = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category

        # Erstellen des Task-Objekts
        task = Task.objects.create(**validated_data)

        # Setzen der Many-to-Many-Beziehung für assignedTo
        task.assignedTo.set(assignedTo_data)

        # Erstellen der Subtasks
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task
    
    
class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'color']