# Generated by Django 4.0 on 2023-11-14 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0013_remove_item_datetime_item_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=2),
        ),
    ]
