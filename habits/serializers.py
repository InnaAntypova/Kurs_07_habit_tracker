from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitValidator


class PrivateHabitsSerializer(serializers.ModelSerializer):
    validators = [HabitValidator()]

    class Meta:
        model = Habit
        fields = '__all__'


class DetailHabitSerializer(serializers.ModelSerializer):
    associated = serializers.SerializerMethodField()

    def get_associated(self, instance):
        """ Метод для получения деталей связанной привычки """
        return PrivateHabitsSerializer(Habit.objects.get(pk=instance.associated.pk)).data

    class Meta:
        model = Habit
        fields = '__all__'


class PublicHabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['place', 'action', 'is_nice', 'periodicity', 'fee']
