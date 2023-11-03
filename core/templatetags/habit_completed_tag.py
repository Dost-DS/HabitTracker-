from django import template
from datetime import date
from datetime import datetime, timedelta

from django.utils import timezone

from core.models import Habit, CompletedTask

register = template.Library()


@register.filter(name='completed_today')
def completed_today(habit, user):

    if habit.frequency == 'weekly':
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
        end_of_week = start_of_week + timedelta(days=6)
        d = CompletedTask.objects.filter(habit=habit, completed_date__range=[start_of_week, end_of_week])
        # Check if the habit has been completed at least once this week by the user
        return CompletedTask.objects.filter(habit=habit, completed_date__range=(start_of_week, end_of_week)).exists()

    return habit.completedtask_set.filter(completed_date=date.today()).exists()
