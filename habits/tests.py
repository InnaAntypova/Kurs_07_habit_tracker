from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from rest_framework import status
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """ Тестирование CRUD для Habit (Привычка) """

    def setUp(self) -> None:
        # пользователь для теста
        self.user = User.objects.create(
            email='test1@test.ru', is_active=True
        )
        # привычка для теста
        self.habit = Habit.objects.create(
            place='test',
            action='test',
            is_nice=True,
            start_time='2024-03-25T19:50:04.914506Z',
            execution_time='100',
            is_published=True,
            user=self.user
        )

    def test_create_habit(self):
        """ Тест на создание привычки """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'улица',
            'action': 'прогулка',
            'is_nice': True,
            'fee': '',
            'start_time': '2024-03-25T19:50:04.914506Z',
            'execution_time': '120',
            'is_published': False,
            'user': 1
        }
        response = self.client.post('/habits/add/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEquals(
            response.json(),
            {'id': 2, 'place': 'улица', 'action': 'прогулка', 'is_nice': True, 'periodicity': 1, 'fee': '',
             'start_time': '2024-03-25T19:50:04.914506Z', 'execution_time': '00:02:00', 'is_published': False,
             'user': 1, 'associated': None}
        )

    def test_get_private_list_habits(self):
        """ Тест на получение списка привычек пользователя """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/my_habits/')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            Habit.objects.all().count(), 1
        )

    def test_get_public_list_habits(self):
        """ Тест на получение списка публичных привычек """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/habits/')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            Habit.objects.all().count(), 1
        )

    def test_detail_habit(self):
        """ Тест на получение детальной информации по одной привычке"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/my_habits/{self.habit.id}/')
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': self.habit.id, 'associated': None, 'place': 'test', 'action': 'test', 'is_nice': True,
             'periodicity': 1, 'fee': None, 'start_time': '2024-03-25T19:50:04.914506Z',
             'execution_time': '00:01:40', 'is_published': True, 'user': self.user.id}
        )

    def test_update_habit(self):
        """ Тест на редактирование привычки """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'test1',
            'start_time': '2024-03-25T21:50:04.914506Z',
            'execution_time': 60
        }
        response = self.client.patch(f'/my_habits/{self.habit.id}/edit/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': self.habit.id, 'place': 'test1', 'action': 'test', 'is_nice': True, 'periodicity': 1,
             'fee': None, 'start_time': '2024-03-25T21:50:04.914506Z', 'execution_time': '00:01:00',
             'is_published': True, 'user': self.user.id, 'associated': None}
        )

    def test_delete_habit(self):
        """ Тест на удаление привычки """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/my_habits/delete/{self.habit.id}/')
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Habit.objects.all().count(), 0
        )


class HabitValidatorsTestCase(APITestCase):
    """ Класс для тестирования валидации данных при создании привычки """
    def setUp(self) -> None:
        # пользователь для теста
        self.user = User.objects.create(
            email='test2@test.ru', is_active=True
        )
        # привычка для теста
        self.habit = Habit.objects.create(
            place='test_place1',
            action='test_action1',
            is_nice=False,
            start_time='2024-03-25T19:50:04.914506Z',
            execution_time='120',
            is_published=False,
            user=self.user
        )

    def test_fee_and_associated_fields(self):
        """ Тест на валидацию заполнения полей associated и fee """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'test_place2',
            'action': 'test_action2',
            'is_nice': False,
            'fee': 'test_fee',
            'start_time': '2024-03-25T19:50:04.914506Z',
            'execution_time': '00:01:00',
            'is_published': False,
            'user': self.user.id,
            'associated': self.habit.id
        }
        response = self.client.post('/habits/add/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEquals(
            response.json(),
            {'non_field_errors': [
                ErrorDetail(string='Нельзя одновременно выбрать связанную привычку и вознаграждение', code='invalid')]}
        )

    def test_is_nice_with_associated(self):
        """ Тест на валидацию связанной привычки """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'test_place2',
            'action': 'test_action2',
            'is_nice': False,
            'start_time': '2024-03-25T19:50:04.914506Z',
            'execution_time': '00:01:00',
            'is_published': False,
            'user': self.user.id,
            'associated': self.habit.id
        }
        response = self.client.post('/habits/add/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEquals(
            response.json(),
            {'non_field_errors': [ErrorDetail(string='В связанные привычки могут попадать только приятные привычки',
                                              code='invalid')]}
        )

    def test_execution_time_field(self):
        """ Тест на валидацию заполнения времени выполнения привычки """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'test_place2',
            'action': 'test_action2',
            'is_nice': False,
            'start_time': '2024-03-25T19:50:04.914506Z',
            'execution_time': '00:03:30',
            'is_published': False,
            'user': self.user.id
        }
        response = self.client.post('/habits/add/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Время выполнения должно быть не больше 2х минут']}
        )

    def test_is_nice_true_field(self):
        """ Тест на валидацию поля is_nice """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'test_place2',
            'action': 'test_action2',
            'is_nice': True,
            'start_time': '2024-03-25T19:50:04.914506Z',
            'execution_time': '00:01:00',
            'is_published': False,
            'user': self.user.id,
            'fee': 'test_fee'
        }
        response = self.client.post('/habits/add/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEquals(
            response.json(),
            {'non_field_errors': [ErrorDetail(string='У приятной привычки не может быть вознаграждения или '
                                                     'связанной привычки', code='invalid')]}
        )

    def test_periodicity(self):
        """ Тест на валидацию периода выполнения привычки """
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'test_place2',
            'action': 'test_action2',
            'is_nice': True,
            'start_time': '2024-03-25T19:50:04.914506Z',
            'execution_time': '00:01:00',
            'is_published': False,
            'user': self.user.id,
            'periodicity': '8'
        }
        response = self.client.post('/habits/add/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEquals(
            response.json(),
            {'non_field_errors': [
                ErrorDetail(string='Нельзя выполнять привычку реже чем 1 раз в 7 дней.', code='invalid')]}
        )
