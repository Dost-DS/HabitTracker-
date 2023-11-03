import datetime
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.forms import HabitForm
from core.models import Habit, CompletedTask
from django.contrib.auth.models import User


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.habit = Habit.objects.create(user=self.user, task='Test Habit', periodicity=3, frequency='weekly')

        self.habit1 = Habit.objects.create(user=self.user, task='Habit 1', periodicity=3, frequency='daily')
        self.habit2 = Habit.objects.create(user=self.user, task='Habit 2', periodicity=2, frequency='daily')
        self.habit3 = Habit.objects.create(user=self.user, task='Habit 3', periodicity=1, frequency='weekly')

    def test_habit_creation(self):
        self.assertEqual(str(self.habit), self.habit.task)

    def test_habit_list_view_for_verified_user(self):
        logged_in = self.client.login(username='testuser', password='password123')

        # Check if login was successful
        self.assertTrue(logged_in)

        response = self.client.get(reverse('habit_list_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Habit')

    def test_habit_form_valid(self):
        form_data = {'task': 'Test Habit', 'periodicity': 3, 'frequency': 'weekly'}
        form = HabitForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_habit_form_invalid(self):
        form_data = {'task': '', 'periodicity': -1, 'frequency': 'invalid_frequency'}
        form = HabitForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_streak_broken_for_daily_habit(self):
        # Log in the user
        self.client.login(username='testuser', password='password123')
        # simulation for two days consecutive streak.
        today = datetime.date.today()
        for day_offset in range(1, 3):
            completed_date = today - datetime.timedelta(days=day_offset)
            self.habit.current_streak += 1
            self.habit.longest_streak += 1
            self.habit.save()
            CompletedTask.objects.create(habit=self.habit, completed_date=completed_date)

        # Visit the habit list view
        response = self.client.get(reverse('habit_list_view'))

        # check the current streak status
        self.assertEqual(self.habit.current_streak, 2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Habit')
        self.assertContains(response, "Current Streak: 2")

        # simulation for broken streak.
        self.habit.completedtask_set.all().delete()
        for day_offset in range(1, 4):
            completed_date = today - datetime.timedelta(days=day_offset)
            if day_offset != 3:  # Simulate habit not completed on the second day
                CompletedTask.objects.create(habit=self.habit, completed_date=completed_date)

            else:
                self.habit.broken = True
                self.habit.save()
                # go to habit list view
                response = self.client.get(reverse('habit_list_view'))
                self.assertEqual(self.habit.broken, True)
                # check the status of streak is broken in the template
                self.assertContains(response, 'Your Streak is Broken.')

    def test_longest_streak(self):
        # Simulate completing habit1 for a streak of 5 days
        for day_offset in range(1, 6):
            completed_date = datetime.date.today() - datetime.timedelta(days=day_offset)
            self.habit.longest_streak += 1
            CompletedTask.objects.create(habit=self.habit, completed_date=completed_date)
        self.habit.save()
        # Check the longest streak for habit1
        self.assertEqual(self.habit.longest_streak, 5)


class CompletedTaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.habit = Habit.objects.create(user=self.user, task='Test Habit', periodicity=3, frequency='weekly')
        self.completed_task = CompletedTask.objects.create(habit=self.habit, completed_date=datetime.date.today())

    def test_completed_task_creation(self):
        self.assertEqual(self.completed_task.habit, self.habit)


class WeeklyHabitStreakTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a weekly habit
        self.weekly_habit = Habit.objects.create(user=self.user, task='Weekly Habit', periodicity=1, frequency='weekly')

    def test_weekly_habit_streak(self):
        # completing the weekly habit for 4 weeks continuously
        today = datetime.date.today()
        for week_offset in range(1, 5):
            # after each loop week offset increase by 7 days
            completed_date = today - datetime.timedelta(weeks=week_offset)
            CompletedTask.objects.create(habit=self.weekly_habit, completed_date=completed_date)
            self.weekly_habit.current_streak += 1
            self.weekly_habit.longest_streak = self.weekly_habit.current_streak
            self.weekly_habit.last_completed_date = completed_date
            self.weekly_habit.save()

        # Check the streak for the weekly habit
        self.assertEqual(self.weekly_habit.longest_streak, 4)

        # Check if the broken flag is False
        self.assertFalse(self.weekly_habit.broken)

        # Check the last completed date
        self.assertEqual(self.weekly_habit.last_completed_date, today - datetime.timedelta(weeks=4))

        # Check the missed completions
        self.assertEqual(self.weekly_habit.missed_completions, 0)

    def test_weekly_streak_break(self):
        today = timezone.now().date()

        # Simulate completing the habit for four weeks consecutively
        for week in range(1, 5):
            completed_date = today - datetime.timedelta(weeks=week)
            CompletedTask.objects.create(habit=self.weekly_habit, completed_date=completed_date)
            self.weekly_habit.current_streak += 1
            self.weekly_habit.longest_streak = self.weekly_habit.current_streak
            self.weekly_habit.last_completed_date = completed_date
            self.weekly_habit.save()

        # Check if the habit is not considered broken after completing for four weeks
        self.assertFalse(self.weekly_habit.broken)

        # Simulate failing to complete the habit in the fifth week
        failed_completion_date = today + datetime.timedelta(weeks=1)

        # Check if the habit is considered broken after failing to complete in the fourth week
        if self.weekly_habit.last_completed_date < failed_completion_date:
            self.assertEqual(self.weekly_habit.longest_streak, 4)
            self.assertEqual(self.weekly_habit.current_streak, 4)
            # broke the streak
            self.weekly_habit.broken = True
            self.assertTrue(self.weekly_habit.broken)
        else:
            self.assertFalse(self.weekly_habit.broken)


class AnalyticsHabitTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password')

    def create_habit_with_streak(self, task_name, streak_length):
        # Create a habit for the test user
        habit = Habit.objects.create(
            user=self.user,
            task=task_name,
            periodicity=1,
            frequency="daily"
        )

        # Simulate completing the habit for the specified streak length
        today = timezone.now().date()
        for day_offset in range(streak_length):
            completed_date = today - datetime.timedelta(days=day_offset)
            CompletedTask.objects.create(habit=habit, completed_date=completed_date)
            habit.current_streak += 1
            habit.longest_streak = habit.current_streak
            habit.save()

        return habit

    def test_fetch_habit_with_longest_streak(self):
        from django.db.models import F
        # Create habits with different streak lengths
        habit_1 = self.create_habit_with_streak('Exercise', 5)  # Streak of 5 days
        habit_2 = self.create_habit_with_streak('Book Reading', 3)  # Streak of 3 days
        habit_3 = self.create_habit_with_streak('Gaming', 7)  # Streak of 7 days

        # Fetch the habit with the longest streak
        longest_streak_habit = Habit.objects.filter(user=self.user).annotate(
            streak_length=F('current_streak')).order_by('-longest_streak').first()

        # Check if the correct habit with the longest streak is fetched
        self.assertEqual(longest_streak_habit.task, habit_3.task)
