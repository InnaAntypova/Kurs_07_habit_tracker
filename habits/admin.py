from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'action', 'start_time', 'execution_time', 'is_nice', 'associated', 'periodicity',
                    'fee', 'is_published')
    list_filter = ('place', 'periodicity', 'is_nice')
    search_fields = ('place', 'action')
