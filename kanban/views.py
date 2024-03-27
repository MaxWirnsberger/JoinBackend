from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .models import MyUser, Task, Subtask
from .serializers import TaskSerializer, SubtaskSerializer


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
        

class SignUpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        password = request.data.get("password")

        if MyUser.objects.filter(email=email).exists():
            return Response(
                {"message": "This email already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        user = MyUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
        
class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserData(APIView):
    def get(self, request):
        user = request.user
        return Response({'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
    
    
class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [] #permissions.IsAuthenticated


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

    def destroy(self, request, pk=None):
        try:
            subtask = Subtask.objects.get(pk=pk)
            subtask.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subtask.DoesNotExist:
            return Response({'detail': 'Subtask not found.'}, status=status.HTTP_404_NOT_FOUND)