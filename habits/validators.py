import datetime
from rest_framework import serializers


class HabitValidator:
    """ Валидация значений при заполнении привычки """

    def __call__(self, field_value):
        if field_value.get('associated') and field_value.get('fee'):
            raise serializers.ValidationError('Нельзя одновременно выбрать связанную привычку и вознаграждение')

        if field_value.get('associated'):
            field = field_value.get('associated')
            # print(field)
            if field.is_nice is False:
                raise serializers.ValidationError('В связанные привычки могут попадать только приятные привычки')

        if field_value.get('execution_time') > field_value.get('start_time') + datetime.timedelta(seconds=120):
            raise serializers.ValidationError('Время выполнения должно быть не больше 2х минут')

        if field_value.get('is_nice'):
            if field_value.get('fee') or field_value.get('associated'):
                raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или '
                                                  'связанной привычки')
