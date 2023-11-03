# Generated by Django 4.2.4 on 2023-08-27 22:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='habit',
            name='current_streak',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='habit',
            name='last_completed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='habit',
            name='longest_streak',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
