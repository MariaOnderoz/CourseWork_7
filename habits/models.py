from datetime import timedelta
from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """Модель привычки"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    place = models.CharField(max_length=100, verbose_name="Место выполнения привычки", **NULLABLE)
    start_time = models.TimeField(verbose_name="Время выполнения привычки")
    action = models.CharField(max_length=200, verbose_name="Дествие привычки")
    is_pleasant = models.BooleanField(default=True, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="Связанная привычка", **NULLABLE)
    periodicity = models.IntegerField(default=1, verbose_name="Периодичность выполнения привычки")
    reward = models.CharField(max_length=100, verbose_name="Вознаграждение", **NULLABLE)
    execution_time = models.DurationField(default=timedelta(minutes=1), verbose_name="Время на выполнение привычки", **NULLABLE)
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    def __str__(self):
        return f"Я булу {self.action} в {self.start_time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


