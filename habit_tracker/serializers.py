from datetime import timedelta

from rest_framework import serializers

from habit_tracker.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("creator",)

    def validate(self, data):
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку"
            )
        return data

    def validate_execution_duration(self, value):
        """
        Альтернативный вариант: валидация конкретного поля
        """
        max_duration = timedelta(seconds=120)
        if value > max_duration:
            raise serializers.ValidationError(
                f"Время выполнения не может превышать 120 секунд. "
                f"Вы указали {value.total_seconds()} секунд."
            )
        return value
