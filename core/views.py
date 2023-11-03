from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView

from core.models import Habit, CompletedTask

from .forms import HabitForm


# Create your views here.

class HabitListView(LoginRequiredMixin, ListView):
    template_name = 'pages/habit_list_page.html'
    context_object_name = 'habit_list'
    form_class = HabitForm
    model = Habit
    success_url = reverse_lazy('habit_list_view')

    def get_queryset(self, *args, **kwargs):
        super().get_queryset()
        qs = self.model.objects.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class HabitCreateView(LoginRequiredMixin, CreateView):
    template_name = 'pages/habit_list_page.html'
    form_class = HabitForm
    model = Habit
    # Redirect URL after successful form submission
    success_url = reverse_lazy('habit_list_view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MarkCompletedView(LoginRequiredMixin, View):
    def get(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        completed_today = habit.completedtask_set.filter(completed_date=timezone.now().date()).exists()

        if not completed_today:
            # Check if the habit was completed yesterday
            completed_yesterday = habit.completedtask_set.filter(
                completed_date=timezone.now().date() - timedelta(days=1)).exists()

            if habit.frequency == 'daily':
                if completed_yesterday:
                    # User completed the habit yesterday, increment streak
                    habit.current_streak += 1
                    habit.broken = False  # Reset broken streak if achieved streak again
                    if habit.current_streak > habit.longest_streak:
                        habit.longest_streak = habit.current_streak
                else:
                    # Habit was not completed yesterday, reset streak and track missed completions
                    habit.current_streak = 1
                    habit.broken = True
                    # Increment missed completions
                    habit.missed_completions += 1

            elif habit.frequency == 'weekly':
                # Calculate the start date of the current week
                current_week_start = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
                week_end = current_week_start + timedelta(days=6)
                # Check if the habit was completed within the current week
                if habit.last_completed_date:
                    # Habit was completed within the current week, increment streak
                    habit.current_streak += 1
                    habit.broken = False  # Reset broken streak if achieved streak again
                    if habit.current_streak > habit.longest_streak:
                        habit.longest_streak = habit.current_streak

                if not habit.last_completed_date:
                    habit.current_streak = 1

                else:
                    # Habit was not completed within the current week, reset streak
                    habit.current_streak = 1
                    habit.broken = False

                    # Check if the habit was missed for the entire week
                    week_end = current_week_start + timedelta(days=6)
                    if habit.last_completed_date and habit.last_completed_date < week_end:
                        # Habit was previously completed within the week, reset missed completions
                        # habit.missed_completions = 0
                        pass
                    else:
                        # Habit was not completed for the entire week, track missed completions
                        habit.broken = True
                        habit.missed_completions += 1
            # Create a CompletedTask instance to mark the habit as completed for today
            CompletedTask.objects.create(habit=habit, completed_date=timezone.now().date())

            # Update the last completed date
            habit.last_completed_date = timezone.now().date()
            habit.save()

        return redirect('habit_list_view')


class AnalyticsQuestionAnswerView(TemplateView):
    template_name = 'pages/habit_analytics.html'  # Create a template for displaying the analytics

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Find the habit with the longest streak
        longest_streak_habit = Habit.objects.filter(user=self.request.user).order_by('-longest_streak').first()

        # Find the habit with the most broken streak
        most_broken_streak_habit = Habit.objects.filter(user=self.request.user).order_by('-missed_completions').first()

        context['longest_streak_habit'] = longest_streak_habit
        context['most_broken_streak_habit'] = most_broken_streak_habit

        return context
