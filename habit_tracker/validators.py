from datetime import timedelta

from rest_framework.exceptions import ValidationError


class ExecutionDurationValidator:
    """
    Время выполнения не должно превышать 120 секунд
    """

    def __call__(self, instance):
        max_duration = timedelta(seconds=120)

        if instance > max_duration:
            raise ValidationError(
                f"Время выполнения не может превышать 120 секунд. Вы указали {instance.execution_duration.total_seconds()} секунд."
            )


class PeriodicityValidator:
    """
    Привычку нельзя выполнять реже, чем 1 раз в 7 дней
    """

    MAX_PERIOD_DAYS = 7

    def __call__(self, instance):
        if instance > self.MAX_PERIOD_DAYS:
            raise ValidationError(
                f"Периодичность выполнения привычки не может превышать {self.MAX_PERIOD_DAYS} дней. Вы указали {instance.periodicity} дней(я)."
            )
