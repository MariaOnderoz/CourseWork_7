from rest_framework import serializers
from habits.models import Habit
from habits.validators import RelatedHabitAndRewardValidator, ExecutionTimeValidator, PleasantHabitValidator, \
    RelatedHabitAndIsPleasantValidator, PeriodicityValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitAndRewardValidator("related_habit", "reward"),
            ExecutionTimeValidator("execution_time"),
            PleasantHabitValidator("is_pleasant", "related_habit", "reward"),
            RelatedHabitAndIsPleasantValidator("related_habit", "is_pleasant"),
            PeriodicityValidator("periodicity"),
        ]


