import datetime
from rest_framework import serializers


class HabitValidator:
    """ Валидация значений при заполнении привычки """

    def __call__(self, field_value):
        if field_value.get('associated') and field_value.get('fee'):
            raise serializers.ValidationError('Нельзя одновременно выбрать связанную привычку и вознаграждение')

        if field_value.get('associated'):
            field = field_value.get('associated')
            if not field.is_nice:
                raise serializers.ValidationError('В связанные привычки могут попадать только приятные привычки')

        if field_value.get('is_nice') and (field_value.get('fee') or field_value.get('associated')):
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')

        if field_value.get('execution_time') > datetime.timedelta(seconds=120):
            raise serializers.ValidationError('Время выполнения должно быть не больше 2х минут')

        if field_value.get('periodicity') and field_value.get('periodicity') > 7:
            raise serializers.ValidationError('Нельзя выполнять привычку реже чем 1 раз в 7 дней.')
