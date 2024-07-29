from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from habits.models import Habit
from habits.serializer import HabitSerializer
from users.permissions import IsOwner
from habits.paginations import CustomPagination


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitListAPIView(ListAPIView):
    """Список привычек пользователя"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner,)
    pagination_class = CustomPagination


class HabitRetrieveAPIView(RetrieveAPIView):
    """Детальная информация о привычке"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


class HabitUpdateAPIView(UpdateAPIView):
    """Редакторование привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


class HabitPublicListAPIView(ListAPIView):
    """Список всех привычек"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
