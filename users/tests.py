from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserTestCase(APITestCase):
    """ Тестирование CRUD пользователя """
    def setUp(self) -> None:
        # пользователь для теста
        self.user = User.objects.create(
            email='test1@test.ru', is_active=True
        )

    def test_registration_user(self):
        """ Тест для регистрации пользователя """
        data = {
            'email': 'test2@test.ru',
            'password': '12345',
            'telegram_id': '52321548'
        }
        response = self.client.post('/users/registration/', data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'message': 'Пользователь создан успешно.'}
        )

    def test_user_update(self):
        """ Тест для редактирования пользователя """
        self.client.force_authenticate(user=self.user)
        data = {
            'telegram_id': '523215456',
            'date_joined': '2024-03-26T08:14:48.502241Z',
        }
        response = self.client.patch(f'/users/edit/{self.user.pk}/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': self.user.id, 'password': '', 'last_login': None, 'first_name': '', 'last_name': '',
             'date_joined': '2024-03-26T08:14:48.502241Z', 'email': 'test1@test.ru', 'avatar': None, 'phone': None,
             'city': None, 'telegram_id': '523215456', 'is_active': True, 'is_staff': False, 'is_superuser': False,
             'groups': [], 'user_permissions': []}
        )

    def test_user_profile(self):
        """ Тест для отображения профиля пользователя """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/users/{self.user.id}/profile/')
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_user(self):
        """ Тест для удаления пользователя """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/users/delete/{self.user.id}/')
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
