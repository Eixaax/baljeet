# Generated by Django 4.0 on 2023-11-19 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myweb', '0016_balance_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='balance',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]