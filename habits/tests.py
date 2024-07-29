from rest_framework.test import APITestCase
from django.urls import reverse
from habits.models import Habit
from users.models import User
from rest_framework import status


class HabitTestCase(APITestCase):
    """Тестирование модели Habit"""

    def setUp(self):
        """Тестирование создания пользователя и Привычки"""

        self.user = User.objects.create(email='test@example.com', password='test123')
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            owner=self.user,
            place='Дом',
            start_time='07:30',
            action='Сделать зарядку',
            is_pleasant=True,
            related_habit=None,
            periodicity=1,
            reward='Чашка кофе',
            execution_time='00:15'
        )

    def test_habit_create(self):
        """Тестирование создания новой привычки"""

        url = reverse('habits:habit_create')
        data = {
            'owner': self.user.id,
            'place': 'Дом',
            'start_time': '07:30',
            'action': 'Сделать зарядку',
            'is_pleasant': True,
            'periodicity': 1,
            'reward': 'Чашка кофе',
            'execution_time': '00:15'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 1)

        url = reverse('habits:habit_create')
        data = {
            'owner': self.user.id,
            'place': 'Квартира',
            'start_time': '17:30',
            'action': 'Принять участие в онлайн-игре',
            'is_pleasant': False,
            'related_habit': self.habit.id,
            'periodicity': 3,
            'reward': 'Подарок на день рождения',
            'execution_time': '00:30'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        """Тестирование получения списка всех привычек"""

        url = reverse('habits:habit_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_retrieve(self):
        """Тестирование получения конкретной привычки"""

        url = reverse('habits:habit_retrieve', args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("owner"), self.user.id)
        self.assertEqual(data.get("place"), self.habit.place)
        self.assertEqual(data.get("start_time"), self.habit.start_time)
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("is_pleasant"), self.habit.is_pleasant)
        self.assertEqual(data.get("related_habit"), self.habit.related_habit.id)
        self.assertEqual(data.get("periodicity"), self.habit.periodicity)
        self.assertEqual(data.get("reward"), self.habit.reward)
        self.assertEqual(data.get("execution_time"), self.habit.execution_time)

    def test_habit_update(self):
        """Тестирование редактирования привычки"""

        url = reverse('habits:habit_update', args=(self.habit.pk,))
        data = {
            'place': 'Квартира',
            'start_time': '17:30',
            'action': 'Принять участие в онлайн-игре',
            'is_pleasant': False,
            'related_habit': self.habit.id,
            'periodicity': 3,
            'reward': 'Подарок на день рождения',
            'execution_time': '00:30'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "Квартира")
        self.assertEqual(data.get("start_time"), "17:30")
        self.assertEqual(data.get("action"), "Принять участие в онлайн-игре")
        self.assertEqual(data.get("is_pleasant"), False)
        self.assertEqual(data.get("related_habit"), self.habit.id)
        self.assertEqual(data.get("periodicity"), 3)
        self.assertEqual(data.get("reward"), "Подарок на день рождения")
        self.assertEqual(data.get("execution_time"), "00:30")

    def test_habit_destroy(self):
        """Тестирование удаления привычки"""

        url = reverse('habits:habit_destroy', args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
