from django.urls import path

from . import views

urlpatterns = [
    path('', views.HabitListView.as_view(), name='habit_list_view'),
    path('add/habit/', views.HabitCreateView.as_view(), name='habit_add_view'),
    path('habit/<int:habit_id>/completed/', views.MarkCompletedView.as_view(), name='mark_completed'),
    path('habit/analytics/', views.AnalyticsQuestionAnswerView.as_view(), name='analytic_question_answer'),

]
