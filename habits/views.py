from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginators import CustomPaginator
from habits.permissions import IsOwner
from habits.serializers import PrivateHabitsSerializer, PublicHabitsSerializer, DetailHabitSerializer


class HabitsListAPIView(generics.ListAPIView):
    """ Представление для списка Habits (привычек) пользователя """
    serializer_class = PrivateHabitsSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsOwner, IsAuthenticated]

    def get_queryset(self):
        queryset = Habit.objects.filter(user=self.request.user)
        return queryset


class PublicHabitsListAPIView(generics.ListAPIView):
    """ Представление для списка публичных привычек """
    serializer_class = PublicHabitsSerializer
    queryset = Habit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class HabitCreateApiView(generics.CreateAPIView):
    """ Представление для создания привычки """
    serializer_class = PrivateHabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user  # создатель текущий пользователь
        new_habit.save()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """ Представление для одной привычки """
    serializer_class = DetailHabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """ Представление для редактирования привычки """
    serializer_class = PrivateHabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]


class HabitDeleteAPIView(generics.DestroyAPIView):
    """ Представление для удаления привычки """
    serializer_class = PrivateHabitsSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]
