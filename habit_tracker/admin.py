from django.contrib import admin

from habit_tracker.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit_action', 'habit_place', 'habit_time', 'creator', 'is_public', 'sign_of_pleasant_habit')
