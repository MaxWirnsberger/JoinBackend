from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from kanban.views import LoginView, SignUpView, LogoutView, UserData, TaskView, SubtaskViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskView)
router.register(r'subtasks', SubtaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('singup/', SignUpView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user-data/', UserData.as_view()),
]
