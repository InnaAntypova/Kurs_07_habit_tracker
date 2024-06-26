from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitValidator


class PrivateHabitsSerializer(serializers.ModelSerializer):
    validators = [HabitValidator()]

    class Meta:
        model = Habit
        fields = ['user', 'place', 'action', 'is_nice', 'associated', 'periodicity', 'fee', 'start_time',
                  'execution_time', 'is_published']


class DetailHabitSerializer(serializers.ModelSerializer):
    associated = serializers.SerializerMethodField()

    def get_associated(self, instance):
        """ Метод для получения деталей связанной привычки """
        if instance.associated:
            return PrivateHabitsSerializer(Habit.objects.get(pk=instance.associated.pk)).data
        return None

    class Meta:
        model = Habit
        fields = ['user', 'place', 'action', 'is_nice', 'associated', 'periodicity', 'fee', 'start_time',
                  'execution_time', 'is_published']


class PublicHabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['place', 'action', 'is_nice', 'periodicity', 'fee']
