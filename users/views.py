from rest_framework import generics, status
from rest_framework.response import Response
from users.models import User
from users.serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUserOwner


class UserRegistrationAPIView(generics.CreateAPIView):
    """ Представление для регистрации нового пользователя """
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.data['password'])  # сделать зашифрованный пароль
            user.is_active = True  # активация пользователя
            user.save()
            return Response({'message': f'Пользователь {user.email} создан успешно.'}, status=status.HTTP_201_CREATED)


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Представление для обновления пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class UserProfileAPIView(generics.RetrieveAPIView):
    """ Представление для отображения профиля пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class UserDeleteAPIView(generics.DestroyAPIView):
    """ Представление для удаления пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]
