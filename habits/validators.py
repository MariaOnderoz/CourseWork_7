from datetime import timedelta

from rest_framework.serializers import ValidationError


class RelatedHabitAndRewardValidator:
    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, habit):
        if habit.get(self.related_habit) and habit.get(self.reward):
            raise ValidationError("В модели не должно быть заполнено одновременно и поле вознаграждения, "
                                  "и поле связанной привычки. Можно заполнить только одно из двух полей!")


class ExecutionTimeValidator:
    def __init__(self, execution_time):
        self.execution_time = execution_time

    def __call__(self, habit):
        if habit.get(self.execution_time) and habit.get(self.execution_time) > timedelta(seconds=120):
            raise ValidationError(f"Время на выполнение привычки не может быть превышать {timedelta}!")


class PleasantHabitValidator:
    def __init__(self, is_pleasant, related_habit, reward):
        self.is_pleasant = is_pleasant
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, habit):
        if habit.get(self.is_pleasant) and habit.get(self.reward) or habit.get(self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки!")


class RelatedHabitAndIsPleasantValidator:
    def __init__(self, related_habit, is_pleasant):
        self.related_habit = related_habit
        self.is_pleasant = is_pleasant

    def __call__(self, habit):
        if habit.get(self.related_habit) and not habit.get(self.is_pleasant):
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки!")


class PeriodicityValidator:
    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, habit):
        if habit.get(self.periodicity) and habit.get(self.periodicity) > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней!")

