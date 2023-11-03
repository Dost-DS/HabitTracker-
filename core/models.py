from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    periodicity = models.PositiveIntegerField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    # Current streak  this habit
    current_streak = models.PositiveIntegerField(default=0)
    # Longest streak achieved for this habit
    longest_streak = models.PositiveIntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)
    broken = models.BooleanField(default=False)

    # this field is for how many times users missed the habit.
    missed_completions = models.PositiveIntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.task


class CompletedTask(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    completed_date = models.DateField()

