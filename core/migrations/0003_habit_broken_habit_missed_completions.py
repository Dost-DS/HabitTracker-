# Generated by Django 4.2.4 on 2023-09-05 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_habit_created_date_habit_current_streak_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='broken',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='habit',
            name='missed_completions',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
