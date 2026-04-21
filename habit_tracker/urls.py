from django.urls import path

from habit_tracker.apps import HabitTrackerConfig
from habit_tracker.views import (
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitPublicListAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
)

app_name = HabitTrackerConfig.name

urlpatterns = [
    path("habit/create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("habits/", HabitListAPIView.as_view(), name="habit-list"),
    path("habits/public/", HabitPublicListAPIView.as_view(), name="habit-list-public"),
    path("habit/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-detail"),
    path("habit/update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("habit/delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="habit-delete"),
]
