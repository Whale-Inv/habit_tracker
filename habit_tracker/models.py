from django.conf import settings
from django.db import models

from habit_tracker.validators import ExecutionDurationValidator, RewardValidator, RelatedHabitValidator, \
    PleasantHabitValidator, PeriodicityValidator


class Habit(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь")
    habit_place = models.CharField(max_length=255, verbose_name="место")
    habit_time = models.DateTimeField(verbose_name="время")
    habit_action = models.TextField(verbose_name="действие")
    sign_of_pleasant_habit = models.BooleanField(default=False, verbose_name="признак приятной привычки")
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="связанная приятная привычка",
        limit_choices_to={'sign_of_pleasant_habit': True},
        related_name='related_to'
    )
    periodicity = models.PositiveIntegerField(
        verbose_name="Периодичность (в днях)",
        help_text="Количество дней между выполнениями привычки. По умолчанию — 1 (ежедневно)",
        default=1,
    )
    reward = models.TextField(
        verbose_name="Вознаграждение",
        help_text="Чем вы себя вознаградите после выполнения привычки? Например: чашка кофе, прогулка, просмотр серии любимого сериала и т.п.",
        blank=True,
        null=True
    )
    execution_duration = models.DurationField(verbose_name="время на выполнение")
    is_public = models.BooleanField(verbose_name="признак публичности")

    def clean(self):
        ExecutionDurationValidator()(self)
        RewardValidator()(self)
        RelatedHabitValidator()(self)
        PleasantHabitValidator()(self)
        PeriodicityValidator()(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.habit_action} в {self.habit_place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
