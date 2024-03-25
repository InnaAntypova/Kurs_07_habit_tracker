from django.urls import path
from habits.apps import HabitsConfig
from habits.views import HabitsListAPIView, PublicHabitsListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDeleteAPIView, HabitCreateApiView

app_name = HabitsConfig.name

urlpatterns = [
    path('my_habits/', HabitsListAPIView.as_view(), name='user_habits'),
    path('habits/', PublicHabitsListAPIView.as_view(), name='public_habits'),
    path('habits/add/', HabitCreateApiView.as_view(), name='add_habit'),
    path('my_habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('my_habits/<int:pk>/edit/', HabitUpdateAPIView.as_view(), name='edit_habit'),
    path('my_habits/delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='delete_habit')
]