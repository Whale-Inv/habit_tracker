from rest_framework import generics

from habit_tracker.models import Habit
from habit_tracker.paginators import HabitPaginator
from habit_tracker.serializers import HabitSerializer
from django.db.models import Q


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(creator=user)


class HabitPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(Q(creator=user) | Q(is_public=True)).distinct()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление привычки
    """

    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(creator=self.request.user)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление привычки
    """

    def get_queryset(self):
        return Habit.objects.filter(creator=self.request.user)
