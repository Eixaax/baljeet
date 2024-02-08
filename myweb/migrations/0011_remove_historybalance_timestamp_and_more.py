# Generated by Django 4.0 on 2023-11-08 13:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0010_item_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historybalance',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='historysavings',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='historybalance',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='historysavings',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
