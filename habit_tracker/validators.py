from datetime import timedelta

from rest_framework.exceptions import ValidationError


class RewardValidator:
    """
        Нельзя одновременно выбирать связанную привычку и вознаграждение
    """

    def __call__(self, instance):
        if instance.related_habit and instance.reward:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку. Выберите что-то одно."
            )


class ExecutionDurationValidator:
    """
        Время выполнения не должно превышать 120 секунд
    """

    def __call__(self, instance):
        max_duration = timedelta(seconds=120)

        if instance.execution_duration > max_duration:
            raise ValidationError(
                f"Время выполнения не может превышать 120 секунд. Вы указали {instance.execution_duration.total_seconds()} секунд."
            )


class RelatedHabitValidator:
    """
        Связанная привычка должна быть приятной
    """

    def __call__(self, instance):
        if instance.related_habit and not instance.related_habit.sign_of_pleasant_habit:
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с признаком 'приятная привычка'."
            )


class PleasantHabitValidator:
    """
        У приятной привычки не может быть вознаграждения или связанной привычки
    """

    def __call__(self, instance):
        if instance.sign_of_pleasant_habit:
            if instance.reward:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения."
                )

            if instance.related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть связанной привычки."
                )


class PeriodicityValidator:
    """
        Привычку нельзя выполнять реже, чем 1 раз в 7 дней
    """

    MAX_PERIOD_DAYS = 7

    def __call__(self, instance):
        if instance.periodicity > self.MAX_PERIOD_DAYS:
            raise ValidationError(
                f"Периодичность выполнения привычки не может превышать {self.MAX_PERIOD_DAYS} дней. Вы указали {instance.periodicity} дней(я)."
            )
