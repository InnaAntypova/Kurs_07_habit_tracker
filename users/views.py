from rest_framework import generics
from rest_framework.response import Response

from users.serializers import UserRegistrationSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """ Представление для регистрации нового пользователя """
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.data['password'])  # сделать зашифрованный пароль
            user.is_active = True  # активация пользователя
            user.save()
        return Response({'message': 'Пользователь создан успешно.'})
